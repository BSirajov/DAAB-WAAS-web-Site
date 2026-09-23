<?php
/**
 * Website feedback validation, respectful-language check, and mail assembly.
 * Used by mail-feedback-send.php. No output on include.
 */
declare(strict_types=1);

require_once __DIR__ . '/mail-input-safety.php';

function daab_feedback_lexicon_path(): string
{
    return __DIR__ . '/i18n/feedback-language.json';
}

function daab_feedback_load_terms(): array
{
    $raw = @file_get_contents(daab_feedback_lexicon_path());
    $data = is_string($raw) ? json_decode($raw, true) : null;
    $grouped = is_array($data) && isset($data['terms']) && is_array($data['terms']) ? $data['terms'] : [];
    $terms = [];
    foreach ($grouped as $list) {
        if (!is_array($list)) {
            continue;
        }
        foreach ($list as $term) {
            $term = daab_feedback_fold_string((string) $term);
            if (mb_strlen($term, 'UTF-8') < 3) {
                continue;
            }
            $terms[$term] = true;
        }
    }
    return array_keys($terms);
}

function daab_feedback_chars(string $text): array
{
    if ($text === '') {
        return [];
    }
    $chars = preg_split('//u', $text, -1, PREG_SPLIT_NO_EMPTY);
    return is_array($chars) ? $chars : [];
}

function daab_feedback_fold_char(string $ch): string
{
    if ($ch === 'İ') {
        return 'i';
    }
    $lower = mb_strtolower($ch, 'UTF-8');
    if (mb_strlen($lower, 'UTF-8') === 1) {
        return $lower;
    }
    $parts = daab_feedback_chars($lower);
    return $parts[0] ?? $ch;
}

function daab_feedback_fold_string(string $text): string
{
    $out = '';
    foreach (daab_feedback_chars($text) as $ch) {
        $out .= daab_feedback_fold_char($ch);
    }
    return $out;
}

function daab_feedback_is_word_char(string $ch): bool
{
    if ($ch === '') {
        return false;
    }
    return (bool) preg_match('/^[\p{L}\p{N}_]$/u', $ch);
}

/**
 * @return list<array{start:int,end:int}>
 */
function daab_feedback_language_spans(string $text, ?array $terms = null): array
{
    $terms = $terms ?? daab_feedback_load_terms();
    if ($text === '' || $terms === []) {
        return [];
    }
    $chars = daab_feedback_chars($text);
    $foldedChars = [];
    foreach ($chars as $ch) {
        $foldedChars[] = daab_feedback_fold_char($ch);
    }
    $folded = implode('', $foldedChars);
    $hits = [];

    foreach ($terms as $term) {
        $termChars = daab_feedback_chars($term);
        $len = count($termChars);
        if ($len < 3 || $len > count($foldedChars)) {
            continue;
        }
        $from = 0;
        $limit = count($foldedChars) - $len;
        while ($from <= $limit) {
            $slice = array_slice($foldedChars, $from, $len);
            if ($slice === $termChars) {
                $before = $from > 0 ? $foldedChars[$from - 1] : '';
                $after = ($from + $len) < count($foldedChars) ? $foldedChars[$from + $len] : '';
                if (!daab_feedback_is_word_char($before) && !daab_feedback_is_word_char($after)) {
                    $hits[] = ['start' => $from, 'end' => $from + $len];
                }
                $from += $len;
                continue;
            }
            $from++;
        }
    }

    $collapsed = [];
    $collapsedMap = [];
    $i = 0;
    $n = count($foldedChars);
    while ($i < $n) {
        $j = $i + 1;
        while ($j < $n && $foldedChars[$j] === $foldedChars[$i]) {
            $j++;
        }
        $run = $j - $i;
        if ($run >= 3) {
            $collapsed[] = $foldedChars[$i];
            $collapsedMap[] = [$i, $j];
        } else {
            for ($k = $i; $k < $j; $k++) {
                $collapsed[] = $foldedChars[$k];
                $collapsedMap[] = [$k, $k + 1];
            }
        }
        $i = $j;
    }
    foreach ($terms as $term) {
        if (strpos($term, ' ') !== false) {
            continue;
        }
        $termChars = daab_feedback_chars($term);
        $len = count($termChars);
        if ($len < 3 || $len > count($collapsed)) {
            continue;
        }
        $from = 0;
        $limit = count($collapsed) - $len;
        while ($from <= $limit) {
            if (array_slice($collapsed, $from, $len) === $termChars) {
                $before = $from > 0 ? $collapsed[$from - 1] : '';
                $after = ($from + $len) < count($collapsed) ? $collapsed[$from + $len] : '';
                if (!daab_feedback_is_word_char($before) && !daab_feedback_is_word_char($after)) {
                    $hits[] = [
                        'start' => $collapsedMap[$from][0],
                        'end' => $collapsedMap[$from + $len - 1][1],
                    ];
                }
                $from += $len;
                continue;
            }
            $from++;
        }
    }

    $leet = [
        '@' => 'a', '0' => 'o', '1' => 'i', '3' => 'e', '$' => 's', '5' => 's', '4' => 'a', '7' => 't',
    ];
    $singleTerms = [];
    foreach ($terms as $term) {
        if (strpos($term, ' ') === false) {
            $singleTerms[$term] = true;
        }
    }
    $tokenStart = null;
    $count = count($chars);
    for ($p = 0; $p <= $count; $p++) {
        $ch = $p < $count ? $chars[$p] : ' ';
        $isSpace = $ch === ' ' || $ch === "\n" || $ch === "\t" || $ch === "\r";
        if (!$isSpace && $tokenStart === null) {
            $tokenStart = $p;
        }
        if ($isSpace && $tokenStart !== null) {
            $token = array_slice($chars, $tokenStart, $p - $tokenStart);
            $hasSymbol = false;
            $letters = '';
            foreach ($token as $tokenChar) {
                $mapped = $leet[$tokenChar] ?? $leet[daab_feedback_fold_char($tokenChar)] ?? null;
                if ($mapped !== null) {
                    $hasSymbol = true;
                    $letters .= $mapped;
                    continue;
                }
                $foldedChar = daab_feedback_fold_char($tokenChar);
                if (daab_feedback_is_word_char($foldedChar)) {
                    $letters .= $foldedChar;
                } else {
                    $hasSymbol = true;
                }
            }
            if ($hasSymbol && isset($singleTerms[$letters]) && mb_strlen($letters, 'UTF-8') >= 3) {
                $hits[] = ['start' => $tokenStart, 'end' => $p];
            }
            $tokenStart = null;
        }
    }

    usort($hits, static function (array $a, array $b): int {
        $len = ($b['end'] - $b['start']) <=> ($a['end'] - $a['start']);
        return $len !== 0 ? $len : ($a['start'] <=> $b['start']);
    });
    $kept = [];
    foreach ($hits as $hit) {
        $overlap = false;
        foreach ($kept as $prev) {
            if ($hit['start'] < $prev['end'] && $hit['end'] > $prev['start']) {
                $overlap = true;
                break;
            }
        }
        if (!$overlap) {
            $kept[] = $hit;
        }
    }
    usort($kept, static function (array $a, array $b): int {
        return $a['start'] <=> $b['start'];
    });
    return $kept;
}

function daab_feedback_field(array $post, string $key): string
{
    if (!isset($post[$key])) {
        return '';
    }
    $value = $post[$key];
    if (is_array($value)) {
        $value = implode(', ', array_map('strval', $value));
    }
    $value = trim((string) $value);
    return str_replace(["\0", "\r"], '', $value);
}

function daab_feedback_safe_filename(string $name): string
{
    $name = str_replace(["\0", "\r", "\n"], '', $name);
    $name = basename($name);
    $name = preg_replace('/[^\w.\- ()\[\]]+/u', '_', $name) ?: 'attachment';
    if (strlen($name) > 140) {
        $ext = pathinfo($name, PATHINFO_EXTENSION);
        $base = substr((string) pathinfo($name, PATHINFO_FILENAME), 0, 110);
        $name = $ext !== '' ? $base . '.' . $ext : $base;
    }
    return $name;
}

/**
 * @param array<string, mixed> $file
 * @return array{name:string,type:string,data:string}|null
 */
function daab_feedback_read_attachment(array $file): ?array
{
    $error = (int) ($file['error'] ?? UPLOAD_ERR_NO_FILE);
    $tmp = (string) ($file['tmp_name'] ?? '');
    if ($error === UPLOAD_ERR_NO_FILE || $tmp === '') {
        return null;
    }
    if ($error === UPLOAD_ERR_INI_SIZE || $error === UPLOAD_ERR_FORM_SIZE) {
        throw new RuntimeException('error:file_size');
    }
    if ($error !== UPLOAD_ERR_OK || !is_uploaded_file($tmp)) {
        throw new RuntimeException('error:file_invalid');
    }
    $size = (int) ($file['size'] ?? 0);
    if ($size <= 0 || $size > 5 * 1024 * 1024) {
        throw new RuntimeException('error:file_size');
    }
    $rawName = (string) ($file['name'] ?? '');
    $name = daab_feedback_safe_filename($rawName);
    $ext = strtolower((string) pathinfo($name, PATHINFO_EXTENSION));
    $allowed = [
        'jpg' => ['image/jpeg'],
        'jpeg' => ['image/jpeg'],
        'png' => ['image/png'],
        'webp' => ['image/webp'],
        'gif' => ['image/gif'],
        'pdf' => ['application/pdf'],
    ];
    if (!isset($allowed[$ext])) {
        throw new RuntimeException('error:file_type');
    }
    $detected = '';
    if (class_exists('finfo')) {
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $detected = (string) $finfo->file($tmp);
    }
    if (
        $detected !== ''
        && $detected !== 'application/octet-stream'
        && !in_array($detected, $allowed[$ext], true)
    ) {
        throw new RuntimeException('error:file_type');
    }
    if ($ext === 'pdf') {
        $head = (string) file_get_contents($tmp, false, null, 0, 5);
        if (strncmp($head, '%PDF-', 5) !== 0) {
            throw new RuntimeException('error:file_type');
        }
    } else {
        $info = @getimagesize($tmp);
        if ($info === false) {
            throw new RuntimeException('error:file_type');
        }
    }
    $data = file_get_contents($tmp);
    if ($data === false || $data === '') {
        throw new RuntimeException('error:file_invalid');
    }
    if (daab_input_file_blocked($rawName, $data, $ext)) {
        throw new RuntimeException('error:file_invalid');
    }
    return [
        'name' => $name,
        'type' => $allowed[$ext][0],
        'data' => $data,
    ];
}

function daab_feedback_valid_email(string $email): bool
{
    return daab_input_valid_email($email);
}

function daab_feedback_valid_name(string $name): bool
{
    return daab_input_valid_name($name);
}

function daab_feedback_text_unsafe(string $value, bool $allowNewlines): bool
{
    return daab_input_text_unsafe($value, $allowNewlines);
}

function daab_feedback_valid_url(string $url): bool
{
    if ($url === '') {
        return true;
    }
    if (strlen($url) > 500 || preg_match('/[\r\n\s]/', $url)) {
        return false;
    }
    if (preg_match('/^(javascript|data):/i', $url)) {
        return false;
    }
    if (isset($url[0]) && $url[0] === '/') {
        return !(isset($url[1]) && $url[1] === '/');
    }
    if (!preg_match('#^https?://#i', $url)) {
        return false;
    }
    return (bool) filter_var($url, FILTER_VALIDATE_URL);
}

/**
 * @param array<string, mixed> $post
 * @param array<string, mixed>|null $file
 * @return array{error:string,spans:array<string,list<array{start:int,end:int}>>,fields:array<string,string>,attachment:?array}
 */
function daab_feedback_validate(array $post, ?array $file = null): array
{
    $empty = [
        'error' => '',
        'spans' => [],
        'fields' => [],
        'attachment' => null,
    ];
    $name = daab_feedback_field($post, 'name');
    $email = daab_feedback_field($post, 'email');
    $type = daab_feedback_field($post, 'feedback_type');
    $subject = daab_feedback_field($post, 'subject');
    $message = daab_feedback_field($post, 'message');
    $pageUrl = daab_feedback_field($post, 'related_url');
    $reply = daab_feedback_field($post, 'want_reply');
    $privacy = daab_feedback_field($post, 'privacy_confirm');
    if ($privacy === '') {
        $privacy = daab_feedback_field($post, 'privacyconfirm');
    }
    $replyYes = in_array(strtolower($reply), ['yes', 'true', '1', 'on'], true);
    $privacyYes = in_array(strtolower($privacy), ['yes', 'true', '1', 'on'], true);
    $types = ['general', 'suggestion', 'technical', 'correction', 'other'];

    if ($name === '' || mb_strlen($name, 'UTF-8') > 120) {
        $empty['error'] = 'error:name';
        return $empty;
    }
    if (!daab_feedback_valid_name($name)) {
        $empty['error'] = 'error:name_invalid';
        return $empty;
    }
    if (daab_respect_offensive($name, true)) {
        $empty['error'] = 'error:respect';
        return $empty;
    }
    if (daab_feedback_text_unsafe($name, false)) {
        $empty['error'] = 'error:unsafe';
        return $empty;
    }
    if ($email === '') {
        $empty['error'] = 'error:email_required';
        return $empty;
    }
    if (mb_strlen($email, 'UTF-8') > 200 || !daab_feedback_valid_email($email)) {
        $empty['error'] = 'error:email';
        return $empty;
    }
    if (!in_array($type, $types, true)) {
        $empty['error'] = 'error:type';
        return $empty;
    }
    if ($subject === '' || mb_strlen($subject, 'UTF-8') > 200) {
        $empty['error'] = 'error:subject';
        return $empty;
    }
    if (daab_respect_offensive($subject, false)) {
        $empty['error'] = 'error:respect';
        return $empty;
    }
    if (daab_feedback_text_unsafe($subject, false)) {
        $empty['error'] = 'error:unsafe';
        return $empty;
    }
    if ($message === '' || mb_strlen($message, 'UTF-8') > 5000) {
        $empty['error'] = 'error:message';
        return $empty;
    }
    if (daab_respect_offensive($message, false)) {
        $empty['error'] = 'error:respect';
        return $empty;
    }
    if (daab_feedback_text_unsafe($message, true)) {
        $empty['error'] = 'error:unsafe';
        return $empty;
    }
    if (!daab_feedback_valid_url($pageUrl)) {
        $empty['error'] = 'error:url';
        return $empty;
    }
    if (!$privacyYes) {
        $empty['error'] = 'error:privacy';
        return $empty;
    }

    $subjectSpans = daab_feedback_language_spans($subject);
    $messageSpans = daab_feedback_language_spans($message);
    if ($subjectSpans !== [] || $messageSpans !== []) {
        $empty['error'] = 'error:language';
        $empty['spans'] = [
            'subject' => $subjectSpans,
            'message' => $messageSpans,
        ];
        return $empty;
    }

    $attachment = null;
    if (is_array($file)) {
        try {
            $attachment = daab_feedback_read_attachment($file);
        } catch (RuntimeException $e) {
            $empty['error'] = $e->getMessage();
            return $empty;
        }
    }

    $empty['fields'] = [
        'name' => $name,
        'email' => $email,
        'feedback_type' => $type,
        'subject' => str_replace("\n", ' ', $subject),
        'message' => $message,
        'related_url' => $pageUrl,
        'want_reply' => $replyYes ? 'yes' : 'no',
        'privacy_confirm' => 'yes',
    ];
    $empty['attachment'] = $attachment;
    return $empty;
}
