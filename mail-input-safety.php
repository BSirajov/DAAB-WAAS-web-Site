<?php
/**
 * Shared checks for visitor-submitted text and files.
 * Used by the feedback, membership, and forum registration handlers.
 */
declare(strict_types=1);

require_once __DIR__ . '/mail-respect.php';

function daab_input_valid_email(string $email): bool
{
    return $email !== ''
        && (bool) filter_var($email, FILTER_VALIDATE_EMAIL)
        && !preg_match('/[\r\n]/', $email);
}

function daab_input_valid_name(string $name): bool
{
    return (bool) preg_match('/^[\p{L}\p{M}][\p{L}\p{M} .\'’-]{0,119}$/u', $name);
}

function daab_input_valid_url(string $url): bool
{
    if ($url === '') {
        return true;
    }
    if (strlen($url) > 500 || preg_match('/[\r\n\s]/', $url)) {
        return false;
    }
    if (preg_match('/^(javascript|data|vbscript):/i', $url)) {
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

function daab_input_has_controls(string $value, bool $allowNewlines): bool
{
    $pattern = $allowNewlines ? '/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/' : '/[\x00-\x1F\x7F]/';
    return (bool) preg_match($pattern, $value);
}

function daab_input_has_markup(string $value): bool
{
    if (preg_match('/<\s*\/?\s*[a-z!]/i', $value)) {
        return true;
    }
    if (preg_match('/(?:javascript|vbscript|data)\s*:/i', $value)) {
        return true;
    }
    if (preg_match('/<\?(?:php|=)?|<%/i', $value)) {
        return true;
    }
    if (preg_match('/\bon(?:error|load|click|mouseover|focus)\s*=/i', $value)) {
        return true;
    }
    if (preg_match('/%3c|&#x?0*60;|&lt;/i', $value)) {
        return true;
    }
    return false;
}

function daab_input_has_injection(string $value): bool
{
    $folded = mb_strtolower($value, 'UTF-8');
    $patterns = [
        '/\bunion\s+select\b/u',
        '/\bdrop\s+table\b/u',
        '/\binsert\s+into\b/u',
        '/\bdelete\s+from\b/u',
        '/\binformation_schema\b/u',
        '/\bxp_cmdshell\b/u',
        '/\binto\s+outfile\b/u',
        '/\bload_file\s*\(/u',
        '/\bor\s+1\s*=\s*1\b/u',
        '/\'\s*or\b/u',
        '/[\'"]\s*;\s*--/u',
        '/\b(?:sleep|benchmark)\s*\(/u',
        '/\b(?:exec|execute)\s*\(/u',
    ];
    foreach ($patterns as $pattern) {
        if (preg_match($pattern, $folded)) {
            return true;
        }
    }
    return false;
}

function daab_input_text_unsafe(string $value, bool $allowNewlines = true): bool
{
    return daab_input_has_controls($value, $allowNewlines)
        || daab_input_has_markup($value)
        || daab_input_has_injection($value);
}

function daab_input_file_blocked(string $filename, string $data, string $ext): bool
{
    if (preg_match('/\.(?:php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i', $filename)) {
        return true;
    }
    if (preg_match('/<\?php|<\?=|<script\b/i', $data)) {
        return true;
    }
    if ($ext === 'pdf' && preg_match('/\/(?:JavaScript|JS)\b/', substr($data, 0, 200000))) {
        return true;
    }
    if ($ext === 'docx' && strpos($data, 'vbaProject') !== false) {
        return true;
    }
    return false;
}

function daab_input_header_name(string $name): string
{
    $name = str_replace(["\0", "\r", "\n", '"', '<', '>'], '', $name);
    return trim($name);
}

function daab_input_fail(string $code): void
{
    http_response_code(400);
    echo $code;
    exit;
}

/**
 * @param array<int, string> $names
 * @param array<int, string> $texts
 */
function daab_input_guard(string $email, array $names, array $texts): void
{
    if (!daab_input_valid_email($email)) {
        daab_input_fail('error:email');
    }
    foreach ($names as $name) {
        if ($name === '') {
            continue;
        }
        if (daab_respect_offensive($name, true)) {
            daab_input_fail('error:respect');
        }
        if (!daab_input_valid_name($name) || daab_input_text_unsafe($name, false)) {
            daab_input_fail('error:unsafe');
        }
    }
    foreach ($texts as $text) {
        if ($text === '') {
            continue;
        }
        if (daab_respect_offensive($text, false)) {
            daab_input_fail('error:respect');
        }
        if (daab_input_text_unsafe($text, true)) {
            daab_input_fail('error:unsafe');
        }
    }
}
