<?php
/**
 * Forum 2026 participant registration mail handler.
 * Included from az/forum/2026/mail.php and en/forum/2026/mail.php
 * (set DAAB_APPLICATION_MAIL_LOCALE first).
 *
 * Distinct from mail-application-send.php so submissions are clearly
 * Forum 2026 participant registrations, not membership applications.
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

function daab_forum_mail_field(string $key): string
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

function daab_forum_mail_line(string $label, string $value): string
{
    $value = trim($value);
    if ($value === '') {
        return '';
    }
    return $label . ': ' . $value . "\n";
}

$honeypot = daab_forum_mail_field('website');
if ($honeypot !== '') {
    http_response_code(200);
    echo 'success';
    exit;
}

$email = daab_forum_mail_field('email');
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo 'error';
    exit;
}

$privacyConfirm = daab_forum_mail_field('privacy_confirm');
if ($privacyConfirm === '') {
    $privacyConfirm = daab_forum_mail_field('privacyconfirm');
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

$firstName = daab_forum_mail_field('first_name') ?: daab_forum_mail_field('name');
$lastName = daab_forum_mail_field('last_name') ?: daab_forum_mail_field('surname');
$fullName = daab_forum_mail_field('full_name');
if ($fullName === '') {
    $fullName = trim($firstName . ' ' . $lastName);
}

$city = daab_forum_mail_field('city');
if ($city === '') {
    $city = daab_forum_mail_field('city_manual');
}
$phoneFull = daab_forum_mail_field('phone_full');
if ($phoneFull === '') {
    $phoneCode = daab_forum_mail_field('phone_code');
    $phoneNumber = daab_forum_mail_field('phone_number');
    $phoneFull = trim($phoneCode . ' ' . $phoneNumber);
}
$fatherName = daab_forum_mail_field('father_name') ?: daab_forum_mail_field('fathername');
$dateOfBirth = daab_forum_mail_field('date_of_birth') ?: daab_forum_mail_field('dob');
$countryOfBirth = daab_forum_mail_field('country_of_birth') ?: daab_forum_mail_field('birthcountry');
$citizenship = daab_forum_mail_field('citizenship');
$genderRaw = strtolower(daab_forum_mail_field('gender'));
$gender = $genderRaw;
if ($genderRaw === 'male') {
    $gender = $isAz ? 'Kişi' : 'Male';
} elseif ($genderRaw === 'female') {
    $gender = $isAz ? 'Qadın' : 'Female';
}
$university = daab_forum_mail_field('university');
$degree = daab_forum_mail_field('degree');
$degreeInstitution = daab_forum_mail_field('degree_institution') ?: daab_forum_mail_field('deginst');
$academicTitle = daab_forum_mail_field('academic_title') ?: daab_forum_mail_field('title');
$titleInstitution = daab_forum_mail_field('title_institution') ?: daab_forum_mail_field('titinst');
$currentJob = daab_forum_mail_field('current_job') ?: daab_forum_mail_field('currentjob') ?: daab_forum_mail_field('affiliation');
$previousJobs = daab_forum_mail_field('previous_jobs') ?: daab_forum_mail_field('prevjobs');
$contributions = daab_forum_mail_field('contributions');
$sciFields = daab_forum_mail_field('sci_fields') ?: daab_forum_mail_field('sci');
$additionalInfo = daab_forum_mail_field('additional_info') ?: daab_forum_mail_field('addinfo');
$cvConfirm = daab_forum_mail_field('cv_confirm') ?: daab_forum_mail_field('cvconfirm');
if ($cvConfirm === 'on') {
    $cvConfirm = 'yes';
}

$subjectPrefix = $isAz ? 'Forum 2026 iştirakçı qeydiyyatı' : 'Forum 2026 participant registration';
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
        'form_kind' => 'Forma növü',
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
        'form_kind' => 'Form kind',
    ];

$fields = [
    'full_name' => $fullName,
    'father_name' => $fatherName,
    'date_of_birth' => $dateOfBirth,
    'country_of_birth' => $countryOfBirth,
    'citizenship' => $citizenship,
    'gender' => $gender,
    'email' => $email,
    'country' => daab_forum_mail_field('country'),
    'city' => $city,
    'phone_full' => $phoneFull,
    'university' => $university,
    'degree' => $degree,
    'degree_institution' => $degreeInstitution,
    'academic_title' => $academicTitle,
    'title_institution' => $titleInstitution,
    'current_job' => $currentJob,
    'previous_jobs' => $previousJobs,
    'contributions' => $contributions,
    'sci_fields' => $sciFields,
    'additional_info' => $additionalInfo,
    'cv_confirm' => $cvConfirm,
    'privacy_confirm' => $privacyConfirm,
    'submitted_at' => daab_forum_mail_field('submitted_at'),
    'page_url' => daab_forum_mail_field('page_url'),
    'form_kind' => daab_forum_mail_field('form_kind') ?: 'forum-2026',
];

$body = ($isAz
    ? "Yeni Forum 2026 iştirakçı qeydiyyatı\n\n"
    : "New Forum 2026 participant registration\n\n");
foreach ($labels as $key => $label) {
    $line = daab_forum_mail_line($label, $fields[$key] ?? '');
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
