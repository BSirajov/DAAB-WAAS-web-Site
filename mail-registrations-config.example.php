<?php
/**
 * Optional. Copy to mail-registrations-config.php on the Hostinger host
 * only if the default folder cannot be created.
 *
 * Default (no config file needed):
 *   /home/.../domains/daab-waas.com/daab-private/
 *   (the folder next to public_html, not inside it)
 *
 * Fallback if that parent folder is not writable:
 *   public_html/daab-private/  (blocked from the web by .htaccess)
 */
declare(strict_types=1);

// define('DAAB_REGISTRATIONS_CSV_DIR', '/home/YOUR_USER/domains/daab-waas.com/daab-private');
