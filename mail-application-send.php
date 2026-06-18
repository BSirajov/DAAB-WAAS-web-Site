<?php
/**
 * Shared membership application mail handler.
 * Included from az/mail.php and en/mail.php (set DAAB_APPLICATION_MAIL_LOCALE first).
 */
declare(strict_types=1);

header('Content-Type: text/plain; charset=UTF-8');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo 'error';
    exit;
}

$locale = defined('DAAB_APPLICATION_MAIL_LOCALE') ? DAAB_APPLICATION_MAIL_LOCALE : 'en';
$isAz = $locale === 'az';

function daab_mail_field(string $key): string
{
    if (!isset($_POST[$key])) {
        return '';
    }
    $value = $_POST[$key];
    if (is_array($value)) {
        $value = implode(', ', array_map('strval', $value));
    }
    $value = trim((string) $value);
    return str_replace(["\0", "\r"], '', $value);
}

function daab_mail_line(string $label, string $value): string
{
    $value = trim($value);
    if ($value === '') {
        return '';
    }
    return $label . ': ' . $value . "\n";
}

$email = daab_mail_field('email');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo 'error';
    exit;
}

$firstName = daab_mail_field('first_name') ?: daab_mail_field('name');
$lastName = daab_mail_field('last_name') ?: daab_mail_field('surname');
$fullName = daab_mail_field('full_name');
if ($fullName === '') {
    $fullName = trim($firstName . ' ' . $lastName);
}

$subjectPrefix = $isAz ? 'DAAB üzvlük müraciəti' : 'WAAS Membership Application';
$subject = $subjectPrefix . ($fullName !== '' ? ' — ' . $fullName : '');

$labels = $isAz
    ? [
        'full_name' => 'Ad, soyad',
        'email' => 'E-məktub',
        'country' => 'Ölkə',
        'city' => 'Şəhər',
        'phone_full' => 'Telefon',
        'university' => 'Universitet',
        'field_of_study' => 'İxtisas sahəsi',
        'degree' => 'Elmi dərəcə',
        'degree_institution' => 'Dərəcə verən müəssisə',
        'academic_title' => 'Elmi ad',
        'title_institution' => 'Elmi ad verən müəssisə',
        'current_job' => 'Hazırkı iş yeri',
        'previous_jobs' => 'Keçmiş iş yerləri',
        'contributions' => 'DAAB-a töhfələr',
        'sci_fields' => 'Elmi sahələr',
        'additional_info' => 'Əlavə məlumat',
        'cv_confirm' => 'CV təsdiqi',
        'submitted_at' => 'Göndərilmə vaxtı',
        'page_url' => 'Səhifə',
    ]
    : [
        'full_name' => 'Full name',
        'email' => 'Email',
        'country' => 'Country',
        'city' => 'City',
        'phone_full' => 'Phone',
        'university' => 'University',
        'field_of_study' => 'Field of study',
        'degree' => 'Degree',
        'degree_institution' => 'Degree institution',
        'academic_title' => 'Academic title',
        'title_institution' => 'Title institution',
        'current_job' => 'Current position',
        'previous_jobs' => 'Previous positions',
        'contributions' => 'Contributions to WAAS',
        'sci_fields' => 'Scientific fields',
        'additional_info' => 'Additional information',
        'cv_confirm' => 'CV confirmation',
        'submitted_at' => 'Submitted at',
        'page_url' => 'Page URL',
    ];

$fields = [
    'full_name' => $fullName,
    'email' => $email,
    'country' => daab_mail_field('country'),
    'city' => daab_mail_field('city'),
    'phone_full' => daab_mail_field('phone_full'),
    'university' => daab_mail_field('university'),
    'field_of_study' => daab_mail_field('field_of_study'),
    'degree' => daab_mail_field('degree'),
    'degree_institution' => daab_mail_field('degree_institution'),
    'academic_title' => daab_mail_field('academic_title'),
    'title_institution' => daab_mail_field('title_institution'),
    'current_job' => daab_mail_field('current_job'),
    'previous_jobs' => daab_mail_field('previous_jobs'),
    'contributions' => daab_mail_field('contributions'),
    'sci_fields' => daab_mail_field('sci_fields'),
    'additional_info' => daab_mail_field('additional_info'),
    'cv_confirm' => daab_mail_field('cv_confirm'),
    'submitted_at' => daab_mail_field('submitted_at'),
    'page_url' => daab_mail_field('page_url'),
];

$body = ($isAz ? "Yeni üzvlük müraciəti\n\n" : "New membership application\n\n");
foreach ($labels as $key => $label) {
    $line = daab_mail_line($label, $fields[$key] ?? '');
    if ($line !== '') {
        $body .= $line;
    }
}

$to = 'info@daab-waas.com';
$fromAddress = 'noreply@daab-waas.com';
$fromName = $isAz ? 'DAAB veb saytı' : 'WAAS website';
$headers = 'From: ' . $fromName . ' <' . $fromAddress . ">\r\n";
$headers .= 'Reply-To: ' . $fullName . ' <' . $email . ">\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

if (@mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers)) {
    echo 'success';
} else {
    http_response_code(500);
    echo 'error';
}
