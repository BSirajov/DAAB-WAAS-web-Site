<?php
/**
 * Server-side respectful-language check.
 * Uses the same list as js/daab-respect.js: i18n/feedback-language.json.
 */
declare(strict_types=1);

function daab_respect_lexicon(): array
{
    static $lexicon = null;
    if ($lexicon !== null) {
        return $lexicon;
    }
    $path = __DIR__ . '/i18n/feedback-language.json';
    $raw = is_file($path) ? file_get_contents($path) : false;
    $data = is_string($raw) ? json_decode($raw, true) : null;
    if (!is_array($data)) {
        $lexicon = ['always' => [], 'contextual' => [], 'frames' => [], 'mentions' => [], 'allow' => []];
        return $lexicon;
    }
    $always = [];
    foreach (($data['terms'] ?? []) as $group) {
        if (!is_array($group)) {
            continue;
        }
        foreach ($group as $term) {
            $folded = daab_respect_fold((string) $term);
            if (mb_strlen($folded, 'UTF-8') >= 3) {
                $always[$folded] = true;
            }
        }
    }
    $lexicon = [
        'always' => array_keys($always),
        'contextual' => daab_respect_fold_list($data['contextual'] ?? []),
        'frames' => daab_respect_fold_list($data['frames'] ?? []),
        'mentions' => daab_respect_fold_list($data['mentions'] ?? []),
        'allow' => array_fill_keys(daab_respect_fold_list($data['allow'] ?? []), true),
    ];
    return $lexicon;
}

function daab_respect_fold(string $text): string
{
    $chars = preg_split('//u', $text, -1, PREG_SPLIT_NO_EMPTY);
    if (!is_array($chars)) {
        return '';
    }
    $out = '';
    foreach ($chars as $ch) {
        if ($ch === 'İ') {
            $out .= 'i';
            continue;
        }
        $lower = mb_strtolower($ch, 'UTF-8');
        $out .= mb_strlen($lower, 'UTF-8') === 1 ? $lower : $ch;
    }
    return $out;
}

/**
 * @param mixed $list
 * @return list<string>
 */
function daab_respect_fold_list($list): array
{
    if (!is_array($list)) {
        return [];
    }
    $seen = [];
    foreach ($list as $term) {
        $folded = daab_respect_fold(trim((string) $term));
        if (mb_strlen($folded, 'UTF-8') >= 3) {
            $seen[$folded] = true;
        }
    }
    return array_keys($seen);
}

function daab_respect_chars(string $text): array
{
    $chars = preg_split('//u', $text, -1, PREG_SPLIT_NO_EMPTY);
    return is_array($chars) ? $chars : [];
}

function daab_respect_is_word(string $ch): bool
{
    return $ch !== '' && (bool) preg_match('/^[\p{L}\p{N}_]$/u', $ch);
}

function daab_respect_offensive(string $text, bool $nameField = false): bool
{
    $folded = daab_respect_fold($text);
    if (mb_strlen(preg_replace('/\s+/u', '', $folded) ?? '', 'UTF-8') < 3) {
        return false;
    }
    $lexicon = daab_respect_lexicon();
    $chars = daab_respect_chars($folded);
    foreach (daab_respect_hits($folded, $chars, $lexicon) as $hit) {
        if (daab_respect_keep($text, $chars, $hit, $nameField, $lexicon)) {
            return true;
        }
    }
    return daab_respect_contextual($text, $chars, $nameField, $lexicon);
}

/**
 * @param array{always:list<string>,allow:array<string,bool>} $lexicon
 * @return list<array{start:int,end:int}>
 */
function daab_respect_hits(string $folded, array $chars, array $lexicon): array
{
    $hits = [];
    foreach ($lexicon['always'] as $term) {
        daab_respect_scan($chars, daab_respect_chars($term), $hits);
    }
    $leet = ['@' => 'a', '0' => 'o', '1' => 'i', '3' => 'e', '$' => 's', '5' => 's', '4' => 'a', '7' => 't', '!' => 'i'];
    $single = [];
    $compact = [];
    foreach ($lexicon['always'] as $term) {
        if (strpos($term, ' ') !== false) {
            $flat = preg_replace('/\s+/u', '', $term) ?? '';
            if (mb_strlen($flat, 'UTF-8') >= 6) {
                $compact[$flat] = true;
            }
            continue;
        }
        $single[$term] = true;
    }
    $count = count($chars);
    $i = 0;
    while ($i < $count) {
        if (!daab_respect_is_word($chars[$i])) {
            $i++;
            continue;
        }
        $j = $i + 1;
        while ($j < $count && daab_respect_is_word($chars[$j])) {
            $j++;
        }
        $token = implode('', array_slice($chars, $i, $j - $i));
        $letters = '';
        $changed = false;
        foreach (daab_respect_chars($token) as $ch) {
            if (isset($leet[$ch])) {
                $letters .= $leet[$ch];
                $changed = true;
            } elseif (daab_respect_is_word($ch)) {
                $letters .= $ch;
            } else {
                $changed = true;
            }
        }
        if ($changed && (isset($single[$letters]) || isset($compact[$letters]))) {
            $hits[] = ['start' => $i, 'end' => $j];
        }
        if (mb_strlen($token, 'UTF-8') >= 4) {
            $squeezed = preg_replace('/(.)\1+/u', '$1', $token) ?? $token;
            if (isset($single[$squeezed])) {
                $hits[] = ['start' => $i, 'end' => $j];
            }
        }
        $i = $j;
    }
    foreach ($lexicon['always'] as $term) {
        if (strpos($term, ' ') !== false || mb_strlen($term, 'UTF-8') < 3) {
            continue;
        }
        daab_respect_separated($chars, daab_respect_chars($term), $hits);
    }
    foreach (preg_split('/\s+/u', $folded) ?: [] as $chunk) {
        if (!is_string($chunk) || mb_strlen($chunk, 'UTF-8') < 3 || !preg_match('/[*._-]/u', $chunk)) {
            continue;
        }
        foreach ($lexicon['always'] as $term) {
            if (strpos($term, ' ') !== false) {
                continue;
            }
            if (daab_respect_mask($chunk, $term)) {
                $byte = strpos($folded, $chunk);
                if ($byte !== false) {
                    $start = mb_strlen(substr($folded, 0, $byte), 'UTF-8');
                    $hits[] = ['start' => $start, 'end' => $start + mb_strlen($chunk, 'UTF-8')];
                }
            }
        }
    }
    return $hits;
}

/**
 * @param list<array{start:int,end:int}> $hits
 */
function daab_respect_scan(array $chars, array $termChars, array &$hits): void
{
    $len = count($termChars);
    $total = count($chars);
    if ($len < 3 || $len > $total) {
        return;
    }
    for ($from = 0; $from <= $total - $len; $from++) {
        if (array_slice($chars, $from, $len) !== $termChars) {
            continue;
        }
        $before = $from > 0 ? $chars[$from - 1] : '';
        $after = ($from + $len) < $total ? $chars[$from + $len] : '';
        if (!daab_respect_is_word($before) && !daab_respect_is_word($after)) {
            $hits[] = ['start' => $from, 'end' => $from + $len];
            $from += $len - 1;
        }
    }
}

/**
 * Match a term when up to two symbols or spaces sit between its letters.
 *
 * @param list<array{start:int,end:int}> $hits
 */
function daab_respect_separated(array $chars, array $termChars, array &$hits): void
{
    $total = count($chars);
    $need = count($termChars);
    if ($need < 3) {
        return;
    }
    for ($start = 0; $start < $total; $start++) {
        if ($chars[$start] !== $termChars[0]) {
            continue;
        }
        if ($start > 0 && daab_respect_is_word($chars[$start - 1])) {
            continue;
        }
        $pos = $start;
        $ok = true;
        for ($n = 1; $n < $need; $n++) {
            $gap = 0;
            $pos++;
            while ($pos < $total && $gap < 2 && !daab_respect_is_word($chars[$pos])) {
                $pos++;
                $gap++;
            }
            if ($pos >= $total || $chars[$pos] !== $termChars[$n]) {
                $ok = false;
                break;
            }
        }
        if (!$ok) {
            continue;
        }
        $end = $pos + 1;
        if ($end < $total && daab_respect_is_word($chars[$end])) {
            continue;
        }
        $hits[] = ['start' => $start, 'end' => $end];
    }
}

function daab_respect_mask(string $token, string $term): bool
{
    $left = daab_respect_chars($token);
    $right = daab_respect_chars($term);
    $leet = ['@' => 'a', '0' => 'o', '1' => 'i', '3' => 'e', '$' => 's', '5' => 's', '4' => 'a', '7' => 't', '!' => 'i'];
    $i = 0;
    $j = 0;
    $leftCount = count($left);
    $rightCount = count($right);
    while ($i < $leftCount && $j < $rightCount) {
        $ch = $left[$i];
        if ($ch === '*' || $ch === '.' || $ch === '_' || $ch === '-' || $ch === '+') {
            $i++;
            $j++;
            continue;
        }
        if (isset($leet[$ch])) {
            $ch = $leet[$ch];
        }
        if ($ch !== $right[$j]) {
            return false;
        }
        $i++;
        $j++;
    }
    return $i === $leftCount && $j === $rightCount;
}

/**
 * @param array{start:int,end:int} $hit
 * @param array{allow:array<string,bool>,mentions:list<string>,frames:list<string>} $lexicon
 */
function daab_respect_keep(string $original, array $chars, array $hit, bool $nameField, array $lexicon): bool
{
    $word = preg_replace('/[^\p{L}\p{N}_]+/u', '', implode('', array_slice($chars, $hit['start'], $hit['end'] - $hit['start']))) ?? '';
    if ($word === '' || isset($lexicon['allow'][$word])) {
        return false;
    }
    if (daab_respect_quoted($original, $hit['start'], $hit['end'])) {
        return false;
    }
    if (!$nameField && daab_respect_near($chars, $hit['start'], $hit['end'], $lexicon['mentions']) && !daab_respect_near($chars, $hit['start'], $hit['end'], $lexicon['frames'])) {
        return false;
    }
    return true;
}

function daab_respect_quoted(string $text, int $start, int $end): bool
{
    $chars = daab_respect_chars($text);
    $pairs = ['"' => '"', '«' => '»', '“' => '”', '„' => '“'];
    $open = -1;
    $openChar = '';
    for ($i = 0; $i < $start && $i < count($chars); $i++) {
        $ch = $chars[$i];
        if ($open === -1 && isset($pairs[$ch])) {
            $open = $i;
            $openChar = $ch;
        } elseif ($open !== -1 && $ch === $pairs[$openChar]) {
            $open = -1;
            $openChar = '';
        }
    }
    if ($open === -1) {
        return false;
    }
    $close = $pairs[$openChar];
    $endQuote = -1;
    for ($j = $end; $j < count($chars); $j++) {
        if ($chars[$j] === $close) {
            $endQuote = $j;
            break;
        }
    }
    if ($endQuote === -1) {
        return false;
    }
    $outside = implode('', array_merge(array_slice($chars, 0, $open), array_slice($chars, $endQuote + 1)));
    $outside = preg_replace('/\s+/u', '', $outside) ?? '';
    return mb_strlen($outside, 'UTF-8') >= 12;
}

/**
 * @param list<string> $words
 */
function daab_respect_near(array $chars, int $start, int $end, array $words): bool
{
    $windowStart = max(0, $start - 48);
    $windowEnd = min(count($chars), $end + 24);
    $slice = implode('', array_slice($chars, $windowStart, $windowEnd - $windowStart));
    foreach ($words as $word) {
        $from = 0;
        $wordLen = mb_strlen($word, 'UTF-8');
        $sliceLen = mb_strlen($slice, 'UTF-8');
        while ($from <= $sliceLen - $wordLen) {
            if (mb_substr($slice, $from, $wordLen, 'UTF-8') === $word) {
                $abs = $windowStart + $from;
                $before = $abs > 0 ? $chars[$abs - 1] : '';
                $afterIndex = $abs + $wordLen;
                $after = $afterIndex < count($chars) ? $chars[$afterIndex] : '';
                if (!daab_respect_is_word($before) && !daab_respect_is_word($after) && ($afterIndex <= $start || $abs >= $end)) {
                    return true;
                }
            }
            $from++;
        }
    }
    return false;
}

/**
 * @param array{contextual:list<string>,frames:list<string>,mentions:list<string>,allow:array<string,bool>} $lexicon
 */
function daab_respect_contextual(string $original, array $chars, bool $nameField, array $lexicon): bool
{
    if ($nameField || $lexicon['contextual'] === []) {
        return false;
    }
    $contextual = array_fill_keys($lexicon['contextual'], true);
    $tokens = [];
    $i = 0;
    $count = count($chars);
    while ($i < $count) {
        if (!daab_respect_is_word($chars[$i])) {
            $i++;
            continue;
        }
        $j = $i + 1;
        while ($j < $count && daab_respect_is_word($chars[$j])) {
            $j++;
        }
        $tokens[] = ['text' => implode('', array_slice($chars, $i, $j - $i)), 'start' => $i, 'end' => $j];
        $i = $j;
    }
    foreach ($tokens as $token) {
        if (!isset($contextual[$token['text']])) {
            continue;
        }
        if (isset($lexicon['allow'][$token['text']])) {
            continue;
        }
        $standalone = count($tokens) === 1;
        $framed = daab_respect_near($chars, $token['start'], $token['end'], $lexicon['frames']);
        if (!$standalone && !$framed) {
            continue;
        }
        if (daab_respect_quoted($original, $token['start'], $token['end'])) {
            continue;
        }
        if (daab_respect_near($chars, $token['start'], $token['end'], $lexicon['mentions']) && !$framed) {
            continue;
        }
        return true;
    }
    return false;
}
