<?php
/**
 * Append one registration/membership row to a private CSV.
 * Preferred location: daab-private/ next to public_html (not on the web).
 * Forum CV/photo copies go in daab-private/forum-2026-files/.
 * Fallback: public_html/daab-private/ with Apache deny rules.
 *
 * Optional override: copy mail-registrations-config.example.php to
 * mail-registrations-config.php and set DAAB_REGISTRATIONS_CSV_DIR.
 */
declare(strict_types=1);

function daab_registration_csv_columns(): array
{
    return [
        'received_at',
        'locale',
        'form_kind',
        'full_name',
        'father_name',
        'date_of_birth',
        'country_of_birth',
        'citizenship',
        'gender',
        'email',
        'country',
        'city',
        'phone_full',
        'university',
        'field_of_study',
        'degree',
        'degree_institution',
        'academic_title',
        'title_institution',
        'current_job',
        'previous_jobs',
        'contributions',
        'sci_fields',
        'additional_info',
        'cv_file',
        'photo_file',
        'page_url',
    ];
}

function daab_registrations_config_load(): void
{
    static $loaded = false;
    if ($loaded) {
        return;
    }
    $loaded = true;
    $config = __DIR__ . '/mail-registrations-config.php';
    if (is_file($config)) {
        require_once $config;
    }
}

function daab_registrations_dir_ready(string $dir): bool
{
    if ($dir === '') {
        return false;
    }
    if (!is_dir($dir)) {
        if (!@mkdir($dir, 0750, true) && !is_dir($dir)) {
            return false;
        }
    }
    return is_writable($dir);
}

function daab_registrations_protect_web_dir(string $dir): void
{
    $htaccess = $dir . DIRECTORY_SEPARATOR . '.htaccess';
    if (!is_file($htaccess)) {
        @file_put_contents(
            $htaccess,
            "Require all denied\n<IfModule !mod_authz_core.c>\nDeny from all\n</IfModule>\n"
        );
    }
    $index = $dir . DIRECTORY_SEPARATOR . 'index.html';
    if (!is_file($index)) {
        @file_put_contents($index, '');
    }
}

function daab_registrations_csv_dir(): string
{
    daab_registrations_config_load();
    if (defined('DAAB_REGISTRATIONS_CSV_DIR')) {
        $configured = rtrim((string) DAAB_REGISTRATIONS_CSV_DIR, "/\\");
        if ($configured !== '' && daab_registrations_dir_ready($configured)) {
            return $configured;
        }
    }

    $aboveWeb = dirname(__DIR__) . DIRECTORY_SEPARATOR . 'daab-private';
    if (daab_registrations_dir_ready($aboveWeb)) {
        return $aboveWeb;
    }

    $insideWeb = __DIR__ . DIRECTORY_SEPARATOR . 'daab-private';
    if (daab_registrations_dir_ready($insideWeb)) {
        daab_registrations_protect_web_dir($insideWeb);
        return $insideWeb;
    }

    return '';
}

function daab_registration_csv_filename(string $kind): string
{
    if ($kind === 'membership') {
        return 'membership-applications.csv';
    }
    if ($kind === 'feedback') {
        return 'website-feedback.csv';
    }
    if ($kind === 'complex-topics') {
        return 'complex-topics-submissions.csv';
    }
    return 'forum-2026-registrations.csv';
}

function daab_feedback_csv_columns(): array
{
    return [
        'received_at',
        'locale',
        'form_kind',
        'name',
        'email',
        'reply_requested',
        'feedback_type',
        'subject',
        'message',
        'page_url',
        'attachment',
    ];
}

function daab_registration_files_subdir(string $kind): string
{
    if ($kind === 'membership') {
        return 'membership-files';
    }
    if ($kind === 'feedback') {
        return 'feedback-files';
    }
    if ($kind === 'complex-topics') {
        return 'complex-topics-files';
    }
    return 'forum-2026-files';
}

function daab_registration_safe_stored_name(string $name): string
{
    $name = str_replace(["\0", "\r", "\n"], '', $name);
    $name = basename($name);
    $name = preg_replace('/[^\w.\- ()\[\]]+/u', '_', $name) ?: 'attachment';
    if (strlen($name) > 80) {
        $ext = pathinfo($name, PATHINFO_EXTENSION);
        $base = substr((string) pathinfo($name, PATHINFO_FILENAME), 0, 60);
        $name = $ext !== '' ? $base . '.' . $ext : $base;
    }
    return $name;
}

function daab_registration_files_dir(string $kind): string
{
    $root = daab_registrations_csv_dir();
    if ($root === '') {
        return '';
    }
    $dir = $root . DIRECTORY_SEPARATOR . daab_registration_files_subdir($kind);
    if (!daab_registrations_dir_ready($dir)) {
        return '';
    }
    $insideWeb = __DIR__ . DIRECTORY_SEPARATOR . 'daab-private';
    $normDir = str_replace('\\', '/', $dir);
    $normInside = str_replace('\\', '/', $insideWeb);
    if (strpos($normDir, $normInside) === 0) {
        daab_registrations_protect_web_dir($dir);
    }
    return $dir;
}

function daab_save_registration_upload(string $formKind, string $role, string $originalName, string $data): string
{
    if ($data === '') {
        return '';
    }
    $dir = daab_registration_files_dir($formKind);
    if ($dir === '') {
        return '';
    }
    $safe = daab_registration_safe_stored_name($originalName);
    $stamp = gmdate('Ymd-His');
    $hash = substr(hash('sha256', $data), 0, 8);
    $role = preg_replace('/[^a-z0-9]+/i', '', $role) ?: 'file';
    $filename = $stamp . '_' . $hash . '_' . $role . '_' . $safe;
    $path = $dir . DIRECTORY_SEPARATOR . $filename;
    if (@file_put_contents($path, $data) === false) {
        return '';
    }
    return daab_registration_files_subdir($formKind) . '/' . $filename;
}

/**
 * @param array<string, string> $row
 */
function daab_append_registration_csv(string $kind, array $row, ?array $columns = null): bool
{
    $dir = daab_registrations_csv_dir();
    if ($dir === '') {
        return false;
    }

    $path = $dir . DIRECTORY_SEPARATOR . daab_registration_csv_filename($kind);
    $columns = $columns ?? daab_registration_csv_columns();
    if (($row['received_at'] ?? '') === '') {
        $row['received_at'] = gmdate('Y-m-d H:i:s') . ' UTC';
    }
    if (($row['form_kind'] ?? '') === '') {
        $row['form_kind'] = $kind;
    }

    $handle = @fopen($path, 'c+');
    if ($handle === false) {
        return false;
    }
    if (!flock($handle, LOCK_EX)) {
        fclose($handle);
        return false;
    }

    $stat = fstat($handle);
    $empty = !$stat || (int) $stat['size'] === 0;
    if ($empty) {
        fwrite($handle, "\xEF\xBB\xBF");
        fputcsv($handle, $columns);
    } else {
        fseek($handle, 0, SEEK_END);
    }

    $line = [];
    foreach ($columns as $key) {
        $value = $row[$key] ?? '';
        $value = str_replace(["\0", "\r"], '', (string) $value);
        $value = trim($value);
        $lead = ltrim($value, " \t");
        if ($lead !== '' && strpos('=+-@', $lead[0]) !== false) {
            $value = "'" . $value;
        }
        $line[] = $value;
    }
    $ok = fputcsv($handle, $line) !== false;
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);
    return $ok;
}
