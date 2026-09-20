<?php
/**
 * Claim a one-time send for an application/registration fingerprint.
 * A second POST with the same key within a few minutes is treated as a
 * duplicate so info@daab-waas.com receives only one copy.
 */
declare(strict_types=1);

function daab_mail_send_path(string $key): string
{
    $safe = hash('sha256', $key);
    return rtrim(sys_get_temp_dir(), DIRECTORY_SEPARATOR) . DIRECTORY_SEPARATOR . 'daab-mail-' . $safe;
}

function daab_claim_mail_send(string $key): bool
{
    $path = daab_mail_send_path($key);
    $handle = @fopen($path, 'c+');
    if ($handle === false) {
        return true;
    }
    if (!flock($handle, LOCK_EX)) {
        fclose($handle);
        return true;
    }
    $previous = (int) trim((string) stream_get_contents($handle));
    $now = time();
    if ($previous > 0 && ($now - $previous) < 180) {
        flock($handle, LOCK_UN);
        fclose($handle);
        return false;
    }
    ftruncate($handle, 0);
    rewind($handle);
    fwrite($handle, (string) $now);
    fflush($handle);
    flock($handle, LOCK_UN);
    fclose($handle);
    return true;
}

function daab_release_mail_send(string $key): void
{
    $path = daab_mail_send_path($key);
    if (is_file($path)) {
        @unlink($path);
    }
}
