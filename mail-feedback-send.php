<?php
/**
 * Website feedback mail handler.
 * Included from az/mail-feedback.php and en/mail-feedback.php
 * (set DAAB_APPLICATION_MAIL_LOCALE first).
 *
 * Uses the same recipient, From address, one-send lock, and private
 * attachment storage as Forum 2026 registration.
 */
declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'error';
    exit;
}

require_once __DIR__ . '/mail-feedback-lib.php';

$locale = defined('DAAB_APPLICATION_MAIL_LOCALE') ? (string) DAAB_APPLICATION_MAIL_LOCALE : 'en';
$isAz = $locale === 'az';

function daab_feedback_fail(string $code, int $status = 400, string $extra = ''): void
{
    http_response_code($status);
    echo $extra !== '' ? $code . "\n" . $extra : $code;
    exit;
}

$honeypot = daab_feedback_field($_POST, 'website');
if ($honeypot !== '') {
    echo 'success';
    exit;
}

$started = (int) daab_feedback_field($_POST, 'form_started');
if ($started > 0) {
    $elapsed = (int) round(microtime(true) * 1000) - $started;
    if ($elapsed >= 0 && $elapsed < 1000) {
        echo 'success';
        exit;
    }
}

$file = isset($_FILES['attachment']) && is_array($_FILES['attachment']) ? $_FILES['attachment'] : null;
try {
    $result = daab_feedback_validate($_POST, $file);
} catch (Throwable $e) {
    daab_feedback_fail('error', 400);
}

if ($result['error'] !== '') {
    $extra = '';
    if ($result['error'] === 'error:language') {
        $extra = json_encode(['spans' => $result['spans']], JSON_UNESCAPED_UNICODE) ?: '';
    }
    daab_feedback_fail($result['error'], 400, $extra);
}

$fields = $result['fields'];
$attachment = $result['attachment'];

$typeLabels = $isAz
    ? [
        'general' => 'Ümumi rəy',
        'suggestion' => 'Təklif',
        'technical' => 'Texniki problem',
        'correction' => 'Məzmun düzəlişi',
        'other' => 'Digər',
    ]
    : [
        'general' => 'General feedback',
        'suggestion' => 'Suggestion',
        'technical' => 'Technical problem',
        'correction' => 'Content correction',
        'other' => 'Other',
    ];
$labels = $isAz
    ? [
        'name' => 'Ad',
        'email' => 'E-poçt',
        'want_reply' => 'Cavab istəyir',
        'feedback_type' => 'Rəy növü',
        'subject' => 'Mövzu',
        'message' => 'Rəy',
        'related_url' => 'Əlaqəli səhifə',
        'attachment' => 'Əlavə',
        'submitted_at' => 'Göndərilmə vaxtı',
        'page_url' => 'Formanın səhifəsi',
        'locale' => 'Dil',
        'form_kind' => 'Forma növü',
    ]
    : [
        'name' => 'Name',
        'email' => 'Email',
        'want_reply' => 'Reply requested',
        'feedback_type' => 'Feedback type',
        'subject' => 'Subject',
        'message' => 'Feedback',
        'related_url' => 'Related page',
        'attachment' => 'Attachment',
        'submitted_at' => 'Submitted at',
        'page_url' => 'Form page',
        'locale' => 'Language',
        'form_kind' => 'Form kind',
    ];

$submittedAt = gmdate('Y-m-d H:i:s') . ' UTC';
$typeLabel = $typeLabels[$fields['feedback_type']] ?? $fields['feedback_type'];
$replyLabel = $fields['want_reply'] === 'yes'
    ? ($isAz ? 'Bəli' : 'Yes')
    : ($isAz ? 'Xeyr' : 'No');

$bodyFields = [
    'name' => $fields['name'],
    'email' => $fields['email'],
    'want_reply' => $replyLabel,
    'feedback_type' => $typeLabel,
    'subject' => $fields['subject'],
    'message' => $fields['message'],
    'related_url' => $fields['related_url'],
    'attachment' => $attachment['name'] ?? '',
    'submitted_at' => $submittedAt,
    'page_url' => daab_feedback_valid_url(daab_feedback_field($_POST, 'page_url'))
        ? daab_feedback_field($_POST, 'page_url')
        : '',
    'locale' => $locale,
    'form_kind' => 'feedback',
];

$body = ($isAz ? "Sayt rəyi\n\n" : "Website feedback\n\n");
foreach ($labels as $key => $label) {
    $value = trim((string) ($bodyFields[$key] ?? ''));
    if ($value === '') {
        continue;
    }
    if ($key === 'message') {
        $body .= $label . ":\n" . $value . "\n\n";
        continue;
    }
    $body .= $label . ': ' . str_replace("\n", ' ', $value) . "\n";
}

require_once __DIR__ . '/mail-send-once.php';
$mailOnceKey = strtolower($fields['email']) . "\n"
    . $fields['feedback_type'] . "\n"
    . $fields['subject'] . "\n"
    . $fields['message'] . "\nfeedback";
if (!daab_claim_mail_send($mailOnceKey)) {
    echo 'success';
    exit;
}

$to = 'info@daab-waas.com';
$fromAddress = 'noreply@daab-waas.com';
$fromName = $isAz ? 'DAAB' : 'WAAS';
$subjectPrefix = $isAz ? 'Sayt rəyi' : 'Website feedback';
$subject = $subjectPrefix . ' — ' . $fields['subject'];
$boundary = '==DAAB_FEEDBACK_' . bin2hex(random_bytes(12));
$headers = 'From: ' . $fromName . ' <' . $fromAddress . ">\r\n";
if ($fields['email'] !== '') {
    $headers .= 'Reply-To: ' . $fields['email'] . "\r\n";
}
$headers .= "MIME-Version: 1.0\r\n";
if ($attachment) {
    $headers .= 'Content-Type: multipart/mixed; boundary="' . $boundary . "\"\r\n";
    $message = '--' . $boundary . "\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $message .= $body . "\r\n";
    $ascii = preg_replace('/[^\x20-\x7E]/', '_', $attachment['name']) ?: 'attachment';
    $encodedName = rawurlencode($attachment['name']);
    $message .= '--' . $boundary . "\r\n";
    $message .= 'Content-Type: ' . $attachment['type'] . '; name="' . $ascii . "\"\r\n";
    $message .= "Content-Transfer-Encoding: base64\r\n";
    $message .= 'Content-Disposition: attachment; filename="' . $ascii . '"; filename*=UTF-8\'\'' . $encodedName . "\r\n\r\n";
    $message .= chunk_split(base64_encode($attachment['data']));
    $message .= '--' . $boundary . "--\r\n";
} else {
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message = $body;
}

$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
if (@mail($to, $encodedSubject, $message, $headers)) {
    require_once __DIR__ . '/mail-registrations-csv.php';
    $csvRow = [
        'received_at' => $submittedAt,
        'locale' => $locale,
        'form_kind' => 'feedback',
        'name' => $fields['name'],
        'email' => $fields['email'],
        'reply_requested' => $fields['want_reply'],
        'feedback_type' => $typeLabel,
        'subject' => $fields['subject'],
        'message' => $fields['message'],
        'page_url' => $bodyFields['related_url'] !== '' ? $bodyFields['related_url'] : $bodyFields['page_url'],
        'attachment' => '',
    ];
    if ($attachment) {
        $saved = daab_save_registration_upload('feedback', 'file', $attachment['name'], $attachment['data']);
        if ($saved !== '') {
            $csvRow['attachment'] = $saved;
        }
    }
    daab_append_registration_csv('feedback', $csvRow, daab_feedback_csv_columns());
    echo 'success';
    exit;
}

daab_release_mail_send($mailOnceKey);
daab_feedback_fail('error:attach', 500);
