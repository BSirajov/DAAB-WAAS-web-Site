<?php
/**
 * Shared membership application mail handler.
 * Included from az/mail.php and en/mail.php (set DAAB_APPLICATION_MAIL_LOCALE first).
 */
declare(strict_types=1);

require_once __DIR__ . '/mail-input-safety.php';

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

/* Honeypot: bots fill "website"; humans leave it empty (field is hidden in CSS). */
$honeypot = daab_mail_field('website');
if ($honeypot !== '') {
    http_response_code(200);
    echo 'success';
    exit;
}

$email = daab_mail_field('email');
if (!daab_input_valid_email($email)) {
    daab_input_fail('error:email');
}

$privacyConfirm = daab_mail_field('privacy_confirm');
if ($privacyConfirm === '') {
    $privacyConfirm = daab_mail_field('privacyconfirm');
}
if ($privacyConfirm === 'on') {
    $privacyConfirm = 'yes';
}
$privacyOk = in_array(strtolower($privacyConfirm), ['yes', 'true', '1', 'on'], true);
if (!$privacyOk) {
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

// Native HTML form field aliases (no-JS progressive enhancement).
$city = daab_mail_field('city');
if ($city === '') {
    $city = daab_mail_field('city_manual');
}
$phoneFull = daab_mail_field('phone_full');
if ($phoneFull === '') {
    $phoneCode = daab_mail_field('phone_code');
    $phoneNumber = daab_mail_field('phone_number');
    $phoneFull = trim($phoneCode . ' ' . $phoneNumber);
}
$fatherName = daab_mail_field('father_name') ?: daab_mail_field('fathername');
$dateOfBirth = daab_mail_field('date_of_birth') ?: daab_mail_field('dob');
$countryOfBirth = daab_mail_field('country_of_birth') ?: daab_mail_field('birthcountry');
$citizenship = daab_mail_field('citizenship');
$genderRaw = strtolower(daab_mail_field('gender'));
$gender = $genderRaw;
if ($genderRaw === 'male') {
    $gender = $isAz ? 'Kişi' : 'Male';
} elseif ($genderRaw === 'female') {
    $gender = $isAz ? 'Qadın' : 'Female';
}
$fieldOfStudy = daab_mail_field('field_of_study') ?: daab_mail_field('fieldofstudy');
$degreeInstitution = daab_mail_field('degree_institution') ?: daab_mail_field('deginst');
$academicTitle = daab_mail_field('academic_title') ?: daab_mail_field('title');
$titleInstitution = daab_mail_field('title_institution') ?: daab_mail_field('titinst');
$currentJob = daab_mail_field('current_job') ?: daab_mail_field('currentjob');
$previousJobs = daab_mail_field('previous_jobs') ?: daab_mail_field('prevjobs');
$sciFields = daab_mail_field('sci_fields') ?: daab_mail_field('sci');
$additionalInfo = daab_mail_field('additional_info') ?: daab_mail_field('addinfo');
$cvConfirm = daab_mail_field('cv_confirm') ?: daab_mail_field('cvconfirm');
if ($cvConfirm === 'on') {
    $cvConfirm = 'yes';
}

$subjectPrefix = $isAz ? 'DAAB üzvlük müraciəti' : 'WAAS Membership Application';
$subject = $subjectPrefix . ($fullName !== '' ? ' — ' . $fullName : '');

$labels = $isAz
    ? [
        'full_name' => 'Ad, soyad',
        'father_name' => 'Atanızın adı',
        'date_of_birth' => 'Doğum tarixiniz',
        'country_of_birth' => 'Doğulduğunuz ölkə',
        'citizenship' => 'Vətəndaşlığınız',
        'gender' => 'Cinsiniz',
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
        'privacy_confirm' => 'Məxfilik bildirişi təsdiqi',
        'submitted_at' => 'Göndərilmə vaxtı',
        'page_url' => 'Səhifə',
    ]
    : [
        'full_name' => 'Full name',
        'father_name' => 'Father’s name',
        'date_of_birth' => 'Date of birth',
        'country_of_birth' => 'Country of birth',
        'citizenship' => 'Citizenship',
        'gender' => 'Gender',
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
        'privacy_confirm' => 'Privacy notice acknowledgment',
        'submitted_at' => 'Submitted at',
        'page_url' => 'Page URL',
    ];

$fields = [
    'full_name' => $fullName,
    'father_name' => $fatherName,
    'date_of_birth' => $dateOfBirth,
    'country_of_birth' => $countryOfBirth,
    'citizenship' => $citizenship,
    'gender' => $gender,
    'email' => $email,
    'country' => daab_mail_field('country'),
    'city' => $city,
    'phone_full' => $phoneFull,
    'university' => daab_mail_field('university'),
    'field_of_study' => $fieldOfStudy,
    'degree' => daab_mail_field('degree'),
    'degree_institution' => $degreeInstitution,
    'academic_title' => $academicTitle,
    'title_institution' => $titleInstitution,
    'current_job' => $currentJob,
    'previous_jobs' => $previousJobs,
    'contributions' => daab_mail_field('contributions'),
    'sci_fields' => $sciFields,
    'additional_info' => $additionalInfo,
    'cv_confirm' => $cvConfirm,
    'privacy_confirm' => $privacyConfirm,
    'submitted_at' => gmdate('Y-m-d H:i:s') . ' UTC',
    'page_url' => daab_input_valid_url(daab_mail_field('page_url')) ? daab_mail_field('page_url') : '',
];

daab_input_guard($email, [$firstName, $lastName, $fatherName, $fullName], array_values($fields));

$body = ($isAz ? "Yeni üzvlük müraciəti\n\n" : "New membership application\n\n");
foreach ($labels as $key => $label) {
    $line = daab_mail_line($label, $fields[$key] ?? '');
    if ($line !== '') {
        $body .= $line;
    }
}

require_once __DIR__ . '/mail-send-once.php';
$mailOnceKey = strtolower($email) . "\n" . $fullName . "\nmembership";
if (!daab_claim_mail_send($mailOnceKey)) {
    echo 'success';
    exit;
}

$to = 'info@daab-waas.com';
$fromAddress = 'noreply@daab-waas.com';
$fromName = $isAz ? 'DAAB' : 'WAAS';
$headers = 'From: ' . $fromName . ' <' . $fromAddress . ">\r\n";
$headers .= 'Reply-To: ' . daab_input_header_name($fullName) . ' <' . $email . ">\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

if (@mail($to, '=?UTF-8?B?' . base64_encode($subject) . '?=', $body, $headers)) {
    require_once __DIR__ . '/mail-registrations-csv.php';
    $csvRow = $fields;
    $csvRow['locale'] = $locale;
    $csvRow['form_kind'] = 'membership';
    $csvRow['received_at'] = gmdate('Y-m-d H:i:s') . ' UTC';
    daab_append_registration_csv('membership', $csvRow);
    echo 'success';
} else {
    daab_release_mail_send($mailOnceKey);
    http_response_code(500);
    echo 'error';
}
