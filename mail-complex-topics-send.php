<?php
/**
 * Complex Topics, Clear Explanations application handler.
 * Included from az/mail-complex-topics.php and en/mail-complex-topics.php
 * (set DAAB_APPLICATION_MAIL_LOCALE first).
 */
declare(strict_types=1);

require_once __DIR__ . '/mail-input-safety.php';

header('Content-Type: text/plain; charset=UTF-8');

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
    http_response_code(405);
    echo 'error';
    exit;
}

$locale = defined('DAAB_APPLICATION_MAIL_LOCALE') ? (string) DAAB_APPLICATION_MAIL_LOCALE : 'en';
$isAz = $locale === 'az';

function daab_ct_field(string $key): string
{
    if (!isset($_POST[$key])) {
        return '';
    }
    $value = $_POST[$key];
    if (is_array($value)) {
        $value = implode(', ', array_map('strval', $value));
    }
    return str_replace(["\0", "\r"], '', trim((string) $value));
}

function daab_ct_valid_dob(string $value): bool
{
    if (!preg_match('/^(\d{2})\/(\d{2})\/(\d{4})$/', $value, $match)) {
        return false;
    }
    $day = (int) $match[1];
    $month = (int) $match[2];
    $year = (int) $match[3];
    if ($year < 1900 || !checkdate($month, $day, $year)) {
        return false;
    }
    $date = DateTime::createFromFormat('!d/m/Y', $value);
    if (!$date) {
        return false;
    }
    $today = new DateTime('today');
    return $date <= $today;
}

function daab_ct_list(string $key): array
{
    if (!isset($_POST[$key])) {
        return [];
    }
    $value = $_POST[$key];
    $items = is_array($value) ? $value : [$value];
    $out = [];
    foreach ($items as $item) {
        $item = str_replace(["\0", "\r", "\n"], '', trim((string) $item));
        if ($item !== '') {
            $out[] = $item;
        }
    }
    return $out;
}

function daab_ct_line(string $label, string $value): string
{
    $value = trim($value);
    if ($value === '') {
        return '';
    }
    return $label . ': ' . $value . "\n";
}

function daab_ct_topics(bool $isAz): array
{
    $en = [
        '1' => 'Generative AI and large language models',
        '2' => 'Algorithms and computational problem-solving',
        '3' => 'Variables, assignment, data types and program state',
        '4' => 'Finding errors, tests and reading error messages',
        '5' => 'Cybersecurity, privacy and safe digital behaviour',
        '6' => 'Data science, interpreting data and visualisation',
        '7' => 'Conditions, Boolean logic and decision-making',
        '8' => 'Loops, repetition and stopping',
        '9' => 'Functions, parameters, return values and scope',
        '10' => 'How the Internet and the Web work',
        '11' => 'Machine learning, training data, models and predictions',
        '12' => 'Data structures and their uses',
        '13' => 'Algorithm efficiency and Big-O',
        '14' => 'Databases, modelling and SQL',
        '15' => 'Object-oriented programming',
        '16' => 'Recursion',
        '17' => 'Memory, references, pointers, the stack and dynamic memory',
        '18' => 'Concurrent, asynchronous and parallel programming',
        '19' => 'Binary numbers and digital representation',
        '20' => 'Web programming, APIs and client–server applications',
        '21' => 'Operating systems, processes, memory and file systems',
        '22' => 'Cloud computing, containers and distributed systems',
        '23' => 'Software engineering, Git and collaborative development',
        '24' => 'Computer architecture, the processor, memory and instructions',
        '25' => 'Dynamic programming and designing complex algorithms',
        '26' => 'Cryptography, encryption, hashing and digital signatures',
        '27' => 'Automata, computability and complexity classes',
        '28' => 'Ethics, algorithmic bias and the social effects of computing',
        '29' => 'Game development and interactive graphics',
        '30' => 'Robotics, physical computing and the Internet of Things',
    ];
    $az = [
        '1' => "Məzmun yaradan süni intellekt və böyük dil modelləri",
        '2' => "Alqoritmlər və məsələlərin kompüter vasitəsilə həlli",
        '3' => "Dəyişənlər, mənimsətmə, verilənlər tipləri və proqramın vəziyyəti",
        '4' => "Proqramda səhvlərin tapılması, testlər və xəta mesajlarının anlaşılması",
        '5' => "Kibertəhlükəsizlik, şəxsi məlumatların məxfiliyi və rəqəmsal mühitdə təhlükəsiz davranış",
        '6' => "Verilənlər elmi, məlumatların təhlili və əyani təqdimatı",
        '7' => "Şərtlər, məntiqi əməliyyatlar və qərarvermə",
        '8' => "Dövrlər, təkrarlama və dayanma şərtləri",
        '9' => "Funksiyalar, parametrlər, qaytarılan qiymətlər və görünmə sahəsi",
        '10' => "İnternet və veb necə işləyir",
        '11' => "Maşın öyrənməsi, təlim verilənləri, modellər və proqnozlar",
        '12' => "Verilənlər strukturları və onların tətbiqi",
        '13' => "Alqoritmlərin səmərəliliyi və böyük O işarələməsi",
        '14' => "Verilənlər bazaları, modelləşdirmə və SQL",
        '15' => "Obyektyönlü proqramlaşdırma",
        '16' => "Rekursiya",
        '17' => "Yaddaş, istinadlar, göstəricilər, stek və dinamik yaddaş",
        '18' => "Tapşırıqların növbələşərək, asinxron və paralel icrası",
        '19' => "İkilik say sistemi və məlumatların rəqəmsal təsviri",
        '20' => "Veb proqramlaşdırma, API və müştəri–server tətbiqləri",
        '21' => "Əməliyyat sistemləri, proseslər, yaddaş və fayl sistemləri",
        '22' => "Bulud hesablamaları, konteynerlər və paylanmış sistemlər",
        '23' => "Proqram mühəndisliyi, Git və birgə proqram hazırlama",
        '24' => "Kompüterin quruluşu, prosessor, yaddaş və əmrlər",
        '25' => "Dinamik proqramlaşdırma və mürəkkəb alqoritmlərin qurulması",
        '26' => "Kriptoqrafiya, şifrələmə, heşləmə və rəqəmsal imza",
        '27' => "Avtomatlar, hesablanabilənlik və mürəkkəblik sinifləri",
        '28' => "Etika, alqoritmik qərəz və kompüter texnologiyalarının cəmiyyətə təsiri",
        '29' => "Oyunların hazırlanması və interaktiv qrafika",
        '30' => "Robototexnika, fiziki qurğuların proqramla idarə edilməsi və əşyaların interneti",
    ];
    return $isAz ? $az : $en;
}

function daab_ct_labels(bool $isAz): array
{
    if ($isAz) {
        return [
            'category' => [
                'pupil' => 'Şagird',
                'student' => 'Tələbə',
                'vocational' => 'Peşə təhsili alan şəxs',
                'teacher' => 'Müəllim və ya təlimçi',
                'lecturer' => 'Ali məktəb müəllimi',
                'scientist' => 'Alim və ya tədqiqatçı',
                'it' => 'İnformasiya texnologiyaları mütəxəssisi',
                'creator' => 'Tədris və maarifləndirici materialların müəllifi',
                'other' => 'Digər',
            ],
            'participation' => [
                'individual' => 'Fərdi',
                'team' => 'Komanda',
            ],
            'audience' => [
                'primary' => 'İbtidai sinif şagirdləri (I–IV siniflər)',
                'lower-secondary' => 'V–IX sinif şagirdləri',
                'upper-secondary' => 'X–XI sinif şagirdləri',
                'college' => 'Peşə təhsili müəssisələrinin və kolleclərin tələbələri',
                'university' => 'Ali məktəb tələbələri',
                'teachers' => 'Müəllimlər və təlimçilər',
                'adult' => 'Yeni biliklər öyrənmək və ya peşəsini dəyişmək istəyən böyüklər',
                'public' => 'Geniş ictimaiyyət',
                'other' => 'Digər auditoriya',
            ],
            'format' => [
                'article' => 'Məqalə',
                'video' => 'Videomühazirə',
                'presentation' => 'Təqdimat',
                'pack' => 'Tədris paketi',
                'cartoon' => 'Tədris cizgi filmi',
                'animation' => 'Animasiya',
                'comic' => 'Komiks',
                'infographic' => 'İnfoqrafika',
                'interactive' => 'İnteraktiv material',
            ],
            'language' => [
                'az' => 'Azərbaycan dili',
                'en' => 'İngilis dili',
                'other' => 'Digər',
            ],
            'ai' => [
                'none' => 'İstifadə olunmayıb',
                'limited' => 'Məhdud istifadə',
                'substantial' => 'Əhəmiyyətli istifadə',
            ],
            'yes' => 'Bəli',
        ];
    }
    return [
        'category' => [
            'pupil' => 'School pupil',
            'student' => 'University or college student',
            'vocational' => 'Vocational learner',
            'teacher' => 'Teacher or trainer',
            'lecturer' => 'University lecturer',
            'scientist' => 'Scientist or researcher',
            'it' => 'IT professional',
            'creator' => 'Educational content creator',
            'other' => 'Other',
        ],
        'participation' => [
            'individual' => 'Individual',
            'team' => 'Team',
        ],
        'audience' => [
            'primary' => 'Primary school pupils (grades I–IV)',
            'lower-secondary' => 'Pupils in grades V–IX',
            'upper-secondary' => 'Pupils in grades X–XI',
            'college' => 'Students at vocational institutions and colleges',
            'university' => 'Higher-education students',
            'teachers' => 'Teachers and trainers',
            'adult' => 'Adults who want to learn something new or change career',
            'public' => 'The general public',
            'other' => 'Other audience',
        ],
        'format' => [
            'article' => 'Article',
            'video' => 'Video lecture',
            'presentation' => 'Presentation',
            'pack' => 'Teaching pack',
            'cartoon' => 'Educational cartoon',
            'animation' => 'Animation',
            'comic' => 'Comic',
            'infographic' => 'Infographic',
            'interactive' => 'Interactive material',
        ],
        'language' => [
            'az' => 'Azerbaijani',
            'en' => 'English',
            'other' => 'Other',
        ],
        'ai' => [
            'none' => 'Not used',
            'limited' => 'Used in a limited way',
            'substantial' => 'Used substantially',
        ],
        'yes' => 'Yes',
    ];
}

function daab_ct_yes(string $value): bool
{
    return in_array(strtolower($value), ['yes', 'true', '1', 'on'], true);
}

function daab_ct_attachment_headers(array $attachment): string
{
    $ascii = preg_replace('/[^\x20-\x7E]/', '_', $attachment['name']) ?: 'attachment';
    $encoded = rawurlencode($attachment['name']);
    return 'Content-Type: ' . $attachment['type'] . '; name="' . $ascii . "\"\r\n"
        . "Content-Transfer-Encoding: base64\r\n"
        . 'Content-Disposition: attachment; filename="' . $ascii . '"; filename*=UTF-8\'\'' . $encoded . "\r\n\r\n";
}

function daab_ct_zip_blocked(string $tmp): bool
{
    if (!class_exists('ZipArchive')) {
        return false;
    }
    $zip = new ZipArchive();
    if ($zip->open($tmp) !== true) {
        return true;
    }
    $blocked = false;
    for ($i = 0; $i < $zip->numFiles; $i++) {
        $name = (string) $zip->getNameIndex($i);
        if (preg_match('/\.(?:php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i', $name)) {
            $blocked = true;
            break;
        }
    }
    $zip->close();
    return $blocked;
}

/**
 * @return array<int, array{name:string,type:string,data:string}>
 */
function daab_ct_read_uploads(): array
{
    if (!isset($_FILES['submission_files'])) {
        return [];
    }
    $bag = $_FILES['submission_files'];
    $names = $bag['name'] ?? [];
    if (!is_array($names)) {
        $names = [$names];
        $bag['type'] = [$bag['type'] ?? ''];
        $bag['tmp_name'] = [$bag['tmp_name'] ?? ''];
        $bag['error'] = [$bag['error'] ?? UPLOAD_ERR_NO_FILE];
        $bag['size'] = [$bag['size'] ?? 0];
    }
    $allowed = [
        'pdf' => 'application/pdf',
        'doc' => 'application/msword',
        'docx' => 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'ppt' => 'application/vnd.ms-powerpoint',
        'pptx' => 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'odt' => 'application/vnd.oasis.opendocument.text',
        'odp' => 'application/vnd.oasis.opendocument.presentation',
        'txt' => 'text/plain',
        'png' => 'image/png',
        'jpg' => 'image/jpeg',
        'jpeg' => 'image/jpeg',
        'webp' => 'image/webp',
        'gif' => 'image/gif',
        'mp4' => 'video/mp4',
        'zip' => 'application/zip',
    ];
    $files = [];
    $count = 0;
    foreach ($names as $index => $rawName) {
        $error = (int) ($bag['error'][$index] ?? UPLOAD_ERR_NO_FILE);
        if ($error === UPLOAD_ERR_NO_FILE) {
            continue;
        }
        $count++;
        if ($count > 3) {
            daab_input_fail('error:file_count');
        }
        if ($error === UPLOAD_ERR_INI_SIZE || $error === UPLOAD_ERR_FORM_SIZE) {
            daab_input_fail('error:file_size');
        }
        if ($error !== UPLOAD_ERR_OK) {
            daab_input_fail('error:file_invalid');
        }
        $size = (int) ($bag['size'][$index] ?? 0);
        if ($size <= 0 || $size > 8 * 1024 * 1024) {
            daab_input_fail('error:file_size');
        }
        $ext = strtolower((string) pathinfo((string) $rawName, PATHINFO_EXTENSION));
        if (!isset($allowed[$ext])) {
            daab_input_fail('error:file_type');
        }
        $tmp = (string) ($bag['tmp_name'][$index] ?? '');
        if ($tmp === '' || !is_uploaded_file($tmp)) {
            daab_input_fail('error:file_invalid');
        }
        if ($ext === 'zip' && daab_ct_zip_blocked($tmp)) {
            daab_input_fail('error:file_invalid');
        }
        $data = file_get_contents($tmp);
        if ($data === false || $data === '') {
            daab_input_fail('error:file_invalid');
        }
        if (daab_input_file_blocked((string) $rawName, $data, $ext)) {
            daab_input_fail('error:file_invalid');
        }
        $safe = preg_replace('/[^\w.\- ()\[\]]+/u', '_', basename((string) $rawName)) ?: ('file.' . $ext);
        $files[] = [
            'name' => $safe,
            'type' => $allowed[$ext],
            'data' => $data,
        ];
    }
    return $files;
}

/**
 * @return array{name:string,type:string,data:string}
 */
function daab_ct_read_photo(): array
{
    if (!isset($_FILES['photo_file']) || !is_array($_FILES['photo_file'])) {
        daab_input_fail('error:photo_missing');
    }
    $file = $_FILES['photo_file'];
    $error = (int) ($file['error'] ?? UPLOAD_ERR_NO_FILE);
    $tmp = (string) ($file['tmp_name'] ?? '');
    if ($error === UPLOAD_ERR_NO_FILE || $tmp === '') {
        daab_input_fail('error:photo_missing');
    }
    if ($error === UPLOAD_ERR_INI_SIZE || $error === UPLOAD_ERR_FORM_SIZE) {
        daab_input_fail('error:photo_size');
    }
    if ($error !== UPLOAD_ERR_OK || !is_uploaded_file($tmp)) {
        daab_input_fail('error:photo_invalid');
    }
    $size = (int) ($file['size'] ?? 0);
    if ($size <= 0 || $size > 5 * 1024 * 1024) {
        daab_input_fail('error:photo_size');
    }
    $rawName = (string) ($file['name'] ?? '');
    if (preg_match('/\.(?:php\d?|phtml|phar|svg|html?|js|exe|dll|sh|bat|cmd|htaccess)(?:\.|$)/i', $rawName)) {
        daab_input_fail('error:photo_type');
    }
    $ext = strtolower((string) pathinfo($rawName, PATHINFO_EXTENSION));
    if (!in_array($ext, ['jpg', 'jpeg', 'png'], true)) {
        daab_input_fail('error:photo_type');
    }
    $detected = '';
    if (class_exists('finfo')) {
        $finfo = new finfo(FILEINFO_MIME_TYPE);
        $detected = (string) $finfo->file($tmp);
    }
    $allowedMimes = ['image/jpeg', 'image/png'];
    if ($detected !== '' && $detected !== 'application/octet-stream' && !in_array($detected, $allowedMimes, true)) {
        daab_input_fail('error:photo_type');
    }
    if (@getimagesize($tmp) === false) {
        daab_input_fail('error:photo_type');
    }
    $data = file_get_contents($tmp);
    if ($data === false || $data === '') {
        daab_input_fail('error:photo_invalid');
    }
    if (daab_input_file_blocked($rawName, $data, $ext)) {
        daab_input_fail('error:photo_invalid');
    }
    $safe = preg_replace('/[^\w.\- ()\[\]]+/u', '_', basename($rawName)) ?: ('photo.' . $ext);
    $mime = in_array($detected, $allowedMimes, true) ? $detected : ($ext === 'png' ? 'image/png' : 'image/jpeg');
    return [
        'name' => $safe,
        'type' => $mime,
        'data' => $data,
    ];
}

if (daab_ct_field('website') !== '') {
    echo 'success';
    exit;
}

$firstName = daab_ct_field('first_name');
$surname = daab_ct_field('surname');
$dateOfBirth = daab_ct_field('dob');
$email = daab_ct_field('email');
$country = daab_ct_field('country');
$city = daab_ct_field('city');
if ($city === '') {
    $city = daab_ct_field('city_manual');
}
$organisation = daab_ct_field('organisation');
$category = daab_ct_field('category');
$categoryOther = daab_ct_field('category_other');
$biography = daab_ct_field('biography');
$participation = daab_ct_field('participation');
$teamName = daab_ct_field('team_name');
$member2Name = daab_ct_field('member2_name');
$member2Email = daab_ct_field('member2_email');
$member3Name = daab_ct_field('member3_name');
$member3Email = daab_ct_field('member3_email');
$topicId = daab_ct_field('topic_id');
$otherTitle = daab_ct_field('other_title');
$otherExplanation = daab_ct_field('other_explanation');
$title = daab_ct_field('submission_title');
$audience = daab_ct_field('audience');
$audienceOther = daab_ct_field('audience_other');
$audienceNote = daab_ct_field('audience_note');
$description = daab_ct_field('description');
$formats = daab_ct_list('formats');
$language = daab_ct_field('submission_language');
$languageOther = daab_ct_field('language_other');
$sources = daab_ct_field('sources');
$aiUse = daab_ct_field('ai_use');
$aiDetail = daab_ct_field('ai_detail');
$interestOnly = daab_ct_yes(daab_ct_field('interest_only'));
$link = daab_ct_field('submission_link');
$pageUrl = daab_ct_field('page_url');

$labels = daab_ct_labels($isAz);
$topics = daab_ct_topics($isAz);

if ($firstName === '' || !daab_input_valid_name($firstName)) {
    daab_input_fail('error:name');
}
if ($surname === '' || !daab_input_valid_name($surname)) {
    daab_input_fail('error:surname');
}
if (!daab_ct_valid_dob($dateOfBirth)) {
    daab_input_fail('error:dob');
}
$fullName = trim($firstName . ' ' . $surname);
if (!daab_input_valid_email($email)) {
    daab_input_fail('error:email');
}
if ($country === '' || $city === '') {
    daab_input_fail('error:place');
}
if (!isset($labels['category'][$category])) {
    daab_input_fail('error:category');
}
if ($category === 'other') {
    if ($categoryOther === '') {
        daab_input_fail('error:category_other');
    }
} else {
    $categoryOther = '';
}
if (!isset($labels['participation'][$participation])) {
    daab_input_fail('error:participation');
}
if ($participation === 'team') {
    if ($teamName === '' || $member2Name === '' || !daab_input_valid_name($member2Name)) {
        daab_input_fail('error:team');
    }
    if ($member3Name !== '' && !daab_input_valid_name($member3Name)) {
        daab_input_fail('error:team');
    }
    if ($member2Email !== '' && !daab_input_valid_email($member2Email)) {
        daab_input_fail('error:email');
    }
    if ($member3Email !== '' && !daab_input_valid_email($member3Email)) {
        daab_input_fail('error:email');
    }
} else {
    $teamName = '';
    $member2Name = '';
    $member2Email = '';
    $member3Name = '';
    $member3Email = '';
}

$topicLabel = '';
$hasCustomTopic = $otherTitle !== '';
$hasListedTopic = $topicId !== '' && $topicId !== 'other' && isset($topics[$topicId]);
if ($hasCustomTopic === $hasListedTopic) {
    daab_input_fail('error:topic');
}
if ($hasCustomTopic) {
    if ($otherExplanation === '') {
        daab_input_fail('error:topic_other');
    }
    $topicId = 'other';
    $topicLabel = $isAz ? 'Başqa mövzu təklifi' : 'Propose another topic';
} else {
    $topicLabel = $topics[$topicId];
    $otherTitle = '';
    $otherExplanation = '';
}

if ($title === '') {
    daab_input_fail('error:title');
}
if (!isset($labels['audience'][$audience])) {
    daab_input_fail('error:audience');
}
if ($audience === 'other') {
    if ($audienceOther === '') {
        daab_input_fail('error:audience_other');
    }
} else {
    $audienceOther = '';
}
if ($description === '') {
    daab_input_fail('error:description');
}
$formatLabels = [];
foreach ($formats as $format) {
    if (!isset($labels['format'][$format])) {
        daab_input_fail('error:format');
    }
    $formatLabels[] = $labels['format'][$format];
}
if ($formatLabels === []) {
    daab_input_fail('error:format');
}
if (!isset($labels['language'][$language])) {
    daab_input_fail('error:language');
}
if ($language === 'other') {
    if ($languageOther === '') {
        daab_input_fail('error:language_other');
    }
} else {
    $languageOther = '';
}
if (!isset($labels['ai'][$aiUse])) {
    daab_input_fail('error:ai');
}
if ($aiUse !== 'none' && $aiDetail === '') {
    daab_input_fail('error:ai');
}
if ($aiUse === 'none') {
    $aiDetail = '';
}

$lengthChecks = [
    [$firstName, 120],
    [$surname, 120],
    [$dateOfBirth, 10],
    [$email, 200],
    [$country, 80],
    [$city, 200],
    [$organisation, 200],
    [$categoryOther, 200],
    [$biography, 1000],
    [$teamName, 120],
    [$member2Name, 120],
    [$member3Name, 120],
    [$otherTitle, 200],
    [$otherExplanation, 1000],
    [$title, 200],
    [$audienceOther, 200],
    [$languageOther, 80],
    [$audienceNote, 300],
    [$description, 5000],
    [$sources, 2000],
    [$aiDetail, 1000],
    [$link, 500],
];
foreach ($lengthChecks as $pair) {
    $value = $pair[0];
    $max = $pair[1];
    $length = function_exists('mb_strlen') ? mb_strlen($value) : strlen($value);
    if ($length > $max) {
        daab_input_fail('error:unsafe');
    }
}

if ($link !== '' && !daab_input_valid_url($link)) {
    daab_input_fail('error:link');
}
if (!daab_input_valid_url($pageUrl)) {
    $pageUrl = '';
}

$files = daab_ct_read_uploads();
if (!$interestOnly && $files === [] && $link === '') {
    daab_input_fail('error:work');
}
$files[] = daab_ct_read_photo();

foreach (['conditions', 'originality', 'attribution', 'publication', 'privacy'] as $confirm) {
    if (!daab_ct_yes(daab_ct_field($confirm))) {
        daab_input_fail('error:' . $confirm);
    }
}

$names = [$firstName, $surname];
if ($member2Name !== '') {
    $names[] = $member2Name;
}
if ($member3Name !== '') {
    $names[] = $member3Name;
}
daab_input_guard($email, $names, [
    $country, $city, $organisation, $categoryOther, $biography, $teamName, $otherTitle, $otherExplanation,
    $title, $audienceOther, $audienceNote, $description, $languageOther, $sources, $aiDetail, $link,
]);

$submittedAt = gmdate('Y-m-d H:i:s') . ' UTC';
$formatText = implode(', ', $formatLabels);
$fileNames = [];
foreach ($files as $file) {
    $fileNames[] = $file['name'];
}

$fields = [
    'first_name' => $firstName,
    'surname' => $surname,
    'date_of_birth' => $dateOfBirth,
    'email' => $email,
    'country' => $country,
    'city' => $city,
    'organisation' => $organisation,
    'category' => $category === 'other'
        ? ($labels['category']['other'] . ' — ' . $categoryOther)
        : $labels['category'][$category],
    'category_other' => $categoryOther,
    'biography' => $biography,
    'participation' => $labels['participation'][$participation],
    'team_name' => $teamName,
    'member2_name' => $member2Name,
    'member2_email' => $member2Email,
    'member3_name' => $member3Name,
    'member3_email' => $member3Email,
    'topic' => $topicLabel,
    'other_title' => $otherTitle,
    'other_explanation' => $otherExplanation,
    'submission_title' => $title,
    'audience' => $audience === 'other'
        ? ($labels['audience']['other'] . ' — ' . $audienceOther)
        : $labels['audience'][$audience],
    'audience_other' => $audienceOther,
    'audience_note' => $audienceNote,
    'description' => $description,
    'formats' => $formatText,
    'submission_language' => $language === 'other'
        ? ($labels['language']['other'] . ' — ' . $languageOther)
        : $labels['language'][$language],
    'language_other' => $languageOther,
    'sources' => $sources,
    'ai_use' => $labels['ai'][$aiUse],
    'ai_detail' => $aiDetail,
    'interest_only' => $interestOnly ? $labels['yes'] : '',
    'submission_link' => $link,
    'files' => implode('; ', $fileNames),
    'submitted_at' => $submittedAt,
    'page_url' => $pageUrl,
];

$bodyLabels = $isAz
    ? [
        'first_name' => 'Ad',
        'surname' => 'Soyad',
        'date_of_birth' => 'Doğum tarixi',
        'email' => 'E-poçt',
        'country' => 'Ölkə',
        'city' => 'Şəhər',
        'organisation' => 'Məktəb, universitet və ya təşkilat',
        'category' => 'İştirakçı qrupu',
        'category_other' => 'Qrupun adı',
        'biography' => 'Qısa tərcümeyi-hal',
        'participation' => 'İştirak forması',
        'team_name' => 'Komandanın adı',
        'member2_name' => '2-ci üzv',
        'member2_email' => '2-ci üzvün e-poçtu',
        'member3_name' => '3-cü üzv',
        'member3_email' => '3-cü üzvün e-poçtu',
        'topic' => 'Mövzu',
        'other_title' => 'Başqa mövzu təklif et',
        'other_explanation' => 'Mövzunun izahı',
        'submission_title' => 'İşin başlığı',
        'audience' => 'Hədəf auditoriyası',
        'audience_other' => 'Digər auditoriya',
        'audience_note' => 'Auditoriya qeydi',
        'description' => 'Qısa təsvir',
        'formats' => 'Format',
        'submission_language' => 'İşin dili',
        'language_other' => 'Digər dil',
        'sources' => 'Əsas mənbələr',
        'ai_use' => 'Süni intellekt',
        'ai_detail' => 'Süni intellektin istifadəsi',
        'interest_only' => 'İlkin maraq',
        'submission_link' => 'Keçid',
        'files' => 'Fayllar',
        'submitted_at' => 'Göndərilmə vaxtı',
        'page_url' => 'Səhifə',
    ]
    : [
        'first_name' => 'Name',
        'surname' => 'Surname',
        'date_of_birth' => 'Date of birth',
        'email' => 'Email',
        'country' => 'Country',
        'city' => 'City',
        'organisation' => 'School, university or organisation',
        'category' => 'Participant group',
        'category_other' => 'Group name',
        'biography' => 'Short biography',
        'participation' => 'Participation',
        'team_name' => 'Team name',
        'member2_name' => 'Member 2',
        'member2_email' => 'Member 2 email',
        'member3_name' => 'Member 3',
        'member3_email' => 'Member 3 email',
        'topic' => 'Topic',
        'other_title' => 'Propose another topic',
        'other_explanation' => 'Why this topic',
        'submission_title' => 'Submission title',
        'audience' => 'Intended audience',
        'audience_other' => 'Other audience',
        'audience_note' => 'Audience note',
        'description' => 'Brief description',
        'formats' => 'Format',
        'submission_language' => 'Submission language',
        'language_other' => 'Other language',
        'sources' => 'Main sources',
        'ai_use' => 'Artificial intelligence',
        'ai_detail' => 'How AI was used',
        'interest_only' => 'Expression of interest',
        'submission_link' => 'Link',
        'files' => 'Files',
        'submitted_at' => 'Submitted at',
        'page_url' => 'Page URL',
    ];

$body = ($isAz
    ? "Yeni müraciət: Çətin mövzu, aydın izah\n\n"
    : "New application: Complex Topics, Clear Explanations\n\n");
foreach ($bodyLabels as $key => $label) {
    $line = daab_ct_line($label, $fields[$key] ?? '');
    if ($line !== '') {
        $body .= $line;
    }
}

require_once __DIR__ . '/mail-send-once.php';
$mailOnceKey = strtolower($email) . "\n" . $title . "\n" . $topicId . "\ncomplex-topics";
if (!daab_claim_mail_send($mailOnceKey)) {
    echo 'success';
    exit;
}

$subjectPrefix = $isAz ? 'DAAB Çətin mövzu, aydın izah' : 'WAAS Complex Topics, Clear Explanations';
$subject = $subjectPrefix . ' — ' . $title;
$to = 'info@daab-waas.com';
$fromName = $isAz ? 'DAAB' : 'WAAS';
$headers = 'From: ' . $fromName . " <noreply@daab-waas.com>\r\n";
$headers .= 'Reply-To: ' . daab_input_header_name($fullName) . ' <' . $email . ">\r\n";
$headers .= "MIME-Version: 1.0\r\n";

if ($files === []) {
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message = $body;
} else {
    $boundary = '==DAAB_CT_' . bin2hex(random_bytes(12));
    $headers .= 'Content-Type: multipart/mixed; boundary="' . $boundary . "\"\r\n";
    $message = '--' . $boundary . "\r\n";
    $message .= "Content-Type: text/plain; charset=UTF-8\r\n";
    $message .= "Content-Transfer-Encoding: 8bit\r\n\r\n";
    $message .= $body . "\r\n";
    foreach ($files as $file) {
        $message .= '--' . $boundary . "\r\n";
        $message .= daab_ct_attachment_headers($file);
        $message .= chunk_split(base64_encode($file['data']));
    }
    $message .= '--' . $boundary . "--\r\n";
}

$encodedSubject = '=?UTF-8?B?' . base64_encode($subject) . '?=';
if (@mail($to, $encodedSubject, $message, $headers)) {
    require_once __DIR__ . '/mail-registrations-csv.php';
    $saved = [];
    foreach ($files as $index => $file) {
        $path = daab_save_registration_upload('complex-topics', 'file' . ($index + 1), $file['name'], $file['data']);
        if ($path !== '') {
            $saved[] = $path;
        }
    }
    $csvRow = $fields;
    $csvRow['received_at'] = $submittedAt;
    $csvRow['locale'] = $locale;
    $csvRow['form_kind'] = 'complex-topics';
    $csvRow['topic_id'] = $topicId;
    $csvRow['files'] = implode('; ', $saved !== [] ? $saved : $fileNames);
    $csvRow['conditions'] = $labels['yes'];
    $csvRow['originality'] = $labels['yes'];
    $csvRow['attribution'] = $labels['yes'];
    $csvRow['publication'] = $labels['yes'];
    $csvRow['privacy'] = $labels['yes'];
    daab_append_registration_csv('complex-topics', $csvRow, [
        'received_at', 'locale', 'form_kind', 'first_name', 'surname', 'date_of_birth', 'email', 'country', 'city',
        'organisation', 'category', 'category_other', 'biography', 'participation', 'team_name',
        'member2_name', 'member2_email', 'member3_name', 'member3_email',
        'topic_id', 'topic', 'other_title', 'other_explanation', 'submission_title',
        'audience', 'audience_other', 'audience_note', 'description', 'formats', 'submission_language', 'language_other', 'sources',
        'ai_use', 'ai_detail', 'interest_only', 'submission_link', 'files',
        'conditions', 'originality', 'attribution', 'publication', 'privacy', 'page_url',
    ]);
    echo 'success';
    exit;
}

daab_release_mail_send($mailOnceKey);
http_response_code(500);
echo 'error:send';
exit;
