<?php
/**
 * Append one registration/membership row to a private CSV.
 * Preferred location: daab-private/ next to public_html (not on the web).
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
    return 'forum-2026-registrations.csv';
}

/**
 * @param array<string, string> $row
 */
function daab_append_registration_csv(string $kind, array $row): bool
{
    $dir = daab_registrations_csv_dir();
    if ($dir === '') {
        return false;
    }

    $path = $dir . DIRECTORY_SEPARATOR . daab_registration_csv_filename($kind);
    $columns = daab_registration_csv_columns();
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
        $line[] = trim($value);
    }
    $ok = fputcsv($handle, $line) !== false;
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);
    return $ok;
}
