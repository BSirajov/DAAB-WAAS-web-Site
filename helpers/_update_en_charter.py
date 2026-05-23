#!/usr/bin/env python3
"""One-shot: replace the English charter body with the canonical text from
en/Charter_EN.docx, keeping the existing section/anchor scaffolding intact.

Run with:  python helpers/_update_en_charter.py
"""
from __future__ import annotations

import re
from html import escape as h
from pathlib import Path

from _paths import ROOT


def p(text: str) -> str:
    """Render a paragraph; preserves Unicode quotes/dashes verbatim."""
    return "<p>" + h(text, quote=False).replace("\n", "<br/>") + "</p>"


def h3(text: str) -> str:
    return "<h3>" + h(text, quote=False) + "</h3>"


def ul(items: list[str]) -> str:
    return "<ul>" + "".join("<li>" + h(item, quote=False) + "</li>" for item in items) + "</ul>"


def ol(items: list[str]) -> str:
    return "<ol>" + "".join("<li>" + h(item, quote=False) + "</li>" for item in items) + "</ol>"


SECTIONS: list[tuple[str, str, str, list[str]]] = [
    # (anchor_id, article_title (.article-separate-title), article_no_label, body_blocks)
    (
        "section-01",
        "Name and headquarters of the Association",
        "Article 1.",
        [
            p('Name of the Association: "WORLD ASSOCIATION OF AZERBAIJANI SCIENTISTS".'),
            p("The headquarters of the Association is ISTANBUL."),
            p("The Association may open branches abroad and within the country."),
        ],
    ),
    (
        "section-02",
        "Purpose, subjects and area of activity",
        "Article 2.",
        [
            p(
                "THE WORLD ASSOCIATION OF AZERBAIJANI SCIENTISTS was established as a union of "
                "Azerbaijani intellectuals living in various countries of the world, with the goal "
                "of supporting Azerbaijan in the preparation and implementation of strategic plans "
                "in science and technology, energy, education, health, social sciences and culture."
            ),
            h3("Subjects and forms of activity pursued by the Association"),
            ol([
                "Conducting research to enable and develop its activities;",
                "Organising training activities such as courses, seminars, conferences and panel discussions;",
                "Providing all kinds of information, documents and publications necessary for the realisation of its purposes; establishing a documentation centre and publishing periodicals such as newspapers, magazines, books and bulletins;",
                "Delivering a healthy working environment to achieve its purpose, and providing all kinds of technical tools, equipment, fixtures and stationery;",
                "Engaging in aid-collection activities, provided that the necessary permissions are obtained, and accepting donations from the home country and abroad;",
                "Establishing and operating economic, commercial and industrial enterprises to provide revenues for achieving the objectives of the Charter;",
                "Organising local offices, establishing and furnishing social and cultural facilities, and making them available for members to spend their free time;",
                "In order to develop and maintain social relations among its members, organising events such as dinner meetings, concerts, balls, performances, exhibitions and trips, and enabling members to benefit from such events;",
                "Purchasing, selling, renting and leasing movable and immovable property needed for the Association's activities and establishing legal ownership rights on immovable property;",
                "Establishing a foundation at home and abroad and, if deemed necessary for the realisation of its purposes, setting up facilities and/or federations or joining an existing federation;",
                "Carrying out international activities by collaborating and/or cooperating with other associations or organisations abroad;",
                "If deemed necessary for achieving its purposes, carrying out joint projects with public and government institutions on issues within their area of activity, without prejudice to the provisions of Law No. 5072 “On the Relations of Associations and Foundations with Government Institutions and Organisations”;",
                "Establishing a fund to meet the essential needs of members in food, clothing, other goods and services, and short-term loans;",
                "Opening branches and representative offices in places deemed necessary;",
                "Creating platforms to achieve a common goal with other associations, foundations, unions and similar non-governmental organisations in areas related to the purpose of the Association and not prohibited by law;",
                "Engaging in all kinds of activities needed to achieve its purpose, provided that they are not prohibited by law.",
            ]),
            h3("Area of activity of the Association"),
            p(
                "As the union of Azerbaijani intellectuals living in various countries, the "
                "Association operates at home and abroad to support Azerbaijan in the preparation "
                "and implementation of strategic plans of the Republic in science and technology, "
                "energy, education, health, social sciences and culture."
            ),
        ],
    ),
    (
        "section-03",
        "Right to become a member and membership procedures",
        "Article 3.",
        [
            p(
                "Every physical individual and legal entity with lawful capacity that accepts to "
                "work in the directions stated above by adopting the objectives and principles of "
                "the Association, and meets the conditions stipulated by the legislation, has the "
                "right to become a member of the Association."
            ),
            p(
                "A membership application submitted in writing to the president of the Association "
                "is considered and decided by the Association's board of directors within thirty "
                "days; the applicant is then notified in writing of the decision to accept the "
                "membership or to reject the request. The full name and other required information "
                "of an applicant whose application is accepted are recorded in the book kept for "
                "this purpose."
            ),
            p(
                "The founders of the Association and the applicants whose applications are "
                "accepted by the board constitute the initial membership of the Association."
            ),
            p(
                "Those who have provided significant material and moral support to the Association "
                "may be accepted as honorary members by decision of the board of directors."
            ),
            p(
                "When the number of branches of the Association is more than three, the membership "
                "records of those registered at the Association headquarters are transferred to the "
                "branches. New membership applications are submitted to the branch. Membership "
                "acceptance and removal procedures are carried out by the branch board of directors "
                "and reported to the Head Office in writing within thirty days at most."
            ),
        ],
    ),
    (
        "section-04",
        "Withdrawal from membership",
        "Article 4.",
        [
            p(
                "Each member has the right to withdraw from the Association by notifying the board "
                "of directors in writing. Exit procedures are deemed completed once the member's "
                "resignation petition reaches the board of directors. Resigning from membership "
                "does not end the member's accumulated debt obligations to the Association."
            ),
        ],
    ),
    (
        "section-05",
        "Removal from membership",
        "Article 5.",
        [
            p("Circumstances necessitating removal from the membership of the Association:"),
            ol([
                "Behaving contrary to the Charter of the Association;",
                "Continuously avoiding assigned tasks;",
                "Failing to pay membership dues within six months despite written warnings;",
                "Not complying with the decisions made by the Association's bodies;",
                "Having lost the membership conditions.",
            ]),
            p(
                "If one of the above-mentioned circumstances is detected, a person may be removed "
                "from membership by decision of the board of directors."
            ),
            p(
                "Those who leave or are expelled from the Association are deleted from the member "
                "registry book and cannot claim rights to the Association's assets."
            ),
        ],
    ),
    (
        "section-06",
        "Governing bodies of the Association",
        "Article 6.",
        [
            p("The organs of the Association are:"),
            ol([
                "General Assembly,",
                "Board of Directors,",
                "Audit Board.",
            ]),
        ],
    ),
    (
        "section-07",
        "General Assembly — formation, meeting time and procedures",
        "Article 7.",
        [
            p(
                "The General Assembly is the highest decision-making body of the Association and "
                "is composed of members registered with the Association. When branches are opened, "
                "with the number of branches up to three, it consists of the members registered at "
                "headquarters and the branches; if the number of branches exceeds three, the "
                "registered members at headquarters are transferred to the branches and the "
                "General Assembly is composed of delegates elected at the general assemblies of "
                "the branches."
            ),
            h3("Meeting time"),
            p(
                "The regular General Assembly convenes every three years, in January, on the day, "
                "place and time determined by the board of directors."
            ),
            p(
                "An extraordinary meeting is called by the board of directors when deemed "
                "necessary by the board of directors or audit board, or upon the written "
                "application of one fifth of the members. If the board of directors does not call "
                "the General Assembly, then upon the application of one of the members, the judge "
                "of peace assigns three members to convene the General Assembly to a meeting."
            ),
            h3("Convening procedures"),
            p(
                "The board of directors prepares the list of members who have the right to attend "
                "the General Assembly. Members must be notified at least fifteen days in advance "
                "of the day, time, place and agenda of the meeting — by announcement in at least "
                "one newspaper or on the Association's website, in writing, by message to the "
                "e-mail address or contact number provided by the member, or via a local mass "
                "media publication. In this call, if the meeting cannot be held due to lack of a "
                "majority, the day, time and place of the second meeting are also stated. The "
                "period between the first and second meeting cannot be less than seven days or "
                "more than sixty days."
            ),
            p(
                "If the meeting is postponed for any reason other than lack of majority, this is "
                "announced to the members in accordance with the call procedure for the first "
                "meeting, stating the reasons for postponement. The second meeting must be held "
                "within six months of the postponement date at the latest. Members are invited to "
                "the second meeting according to the principles specified in the first paragraph."
            ),
            p("The General Assembly meeting cannot be postponed more than once."),
            h3("Meeting procedures"),
            p(
                "The General Assembly convenes with the quorum of an absolute majority of the "
                "members who have the right to participate, and — in cases of amendment of the "
                "Charter and dissolution of the Association — with two thirds of the members who "
                "have the right to participate. If the meeting is postponed due to lack of "
                "majority, no majority is required at the second meeting; however, the number of "
                "members attending this meeting cannot be less than twice the total number of "
                "members of the board of directors and the audit board combined."
            ),
            p(
                "The list of members entitled to attend the General Assembly is kept ready at the "
                "meeting place. The identity documents of the members entering are checked by the "
                "members of the board of directors or by the officers appointed by the board. "
                "Members enter the meeting place by signing the attendance list prepared by the "
                "board of directors."
            ),
            p(
                "If the meeting quorum is met, the situation is indicated in the minutes and the "
                "meeting is opened by the chairman of the board of directors, or by a member of "
                "the board assigned by the chairman. If the meeting quorum is not met, the board "
                "of directors prepares the minutes accordingly."
            ),
            p(
                "After the opening, a council committee consisting of a chairman, a sufficient "
                "number of vice-chairmen and a secretary is elected to manage the meeting."
            ),
            p(
                "In votes held for the election of the organs of the Association, voting members "
                "are required to show their identity documents to the council committee and to "
                "sign against their name on the list of attendees."
            ),
            p("The chairman of the council is responsible for the management and security of the meeting."),
            p(
                "At the General Assembly only items on the agenda are discussed. However, issues "
                "requested in writing by one tenth of the members present at the meeting must also "
                "be included in the agenda."
            ),
            p(
                "Each member has one vote in the General Assembly; the member must vote in person. "
                "Honorary members may attend general meetings but cannot vote. If a legal entity is "
                "a member, the chairman of the board of directors of the legal entity, or the "
                "person assigned to represent it, votes on its behalf."
            ),
            p(
                "The issues discussed and decisions taken at the meeting are written in minutes "
                "signed jointly by the chairman of the council and the secretary. At the end of "
                "the meeting, minutes and other documents are delivered to the chairman of the "
                "board of directors, who is responsible for safeguarding these documents and "
                "delivering them to the newly elected board of directors within seven days."
            ),
        ],
    ),
    (
        "section-08",
        "Voting and decision-making procedures of the General Assembly",
        "Article 8.",
        [
            p(
                "At the General Assembly, unless an opposite decision is made, votes are taken "
                "openly. In open voting, the method specified by the chairman of the General "
                "Assembly is applied."
            ),
            p(
                "In the case of secret voting, the papers bearing the seal of the Chairman of the "
                "General Assembly, or the election ballots, are thrown into an empty container "
                "after the members have completed the necessary actions; after voting ends, an "
                "open count is held and the result is determined."
            ),
            p(
                "Decisions at a meeting of the General Assembly are made by the absolute majority "
                "of the members present at the meeting. However, decisions on changes to the "
                "Charter and on dissolution of the Association can only be taken with a two-thirds "
                "majority of the members present at the meeting."
            ),
            h3("Decisions made without a meeting or convocation"),
            p(
                "Decisions made with the written participation of all members without coming "
                "together — and decisions taken by all members of the Association without "
                "following the convening procedure established in this Charter — are valid. "
                "However, decision-making in this manner does not replace the highest meeting of "
                "the General Assembly."
            ),
        ],
    ),
    (
        "section-09",
        "Responsibilities and powers of the General Assembly",
        "Article 9.",
        [
            p("The following issues are discussed and decided by the General Assembly:"),
            ol([
                "Electing the organs of the Association;",
                "Amending the charter of the Association;",
                "Discussing the reports of the board of directors and audit board, and acquitting the board of directors;",
                "Discussing the budget prepared by the board of directors and accepting it as is or with modifications;",
                "Supervising other organs of the Association and, when deemed necessary, dismissing them for reasons;",
                "Considering and deciding on objections raised against decisions of the board of directors to refuse membership or expel members;",
                "Authorising the board of directors to acquire real estate needed for the Association, or to sell existing real estate;",
                "Examining and approving the regulations to be prepared by the board of directors regarding the activities of the Association, either as they are or with amendments;",
                "Determining wages and all types of allowances, daily and travel allowances and compensation to be paid to the chairman and members of the Association's board of directors and audit board who are not government officials;",
                "Deciding whether the Association will join or leave a federation;",
                "Deciding to open the branches or departments of the Association and authorising the board of directors to carry out the related transactions;",
                "Deciding that the Association will carry out international activities and join or leave foreign associations and organisations;",
                "Deciding that the Association will establish a foundation;",
                "Dissolution of the Association;",
                "Considering and adopting decisions on other proposals of the board of directors;",
                "Acting as the highest authorised body of the Association, performing tasks and exercising powers that are not given to any other organ of the Association;",
                "Fulfilling other duties specified in the legislation for the General Assembly.",
            ]),
        ],
    ),
    (
        "section-10",
        "Establishment, responsibilities and powers of the Board of Directors",
        "Article 10.",
        [
            p(
                "The board of directors, consisting of five main and five substitute members, is "
                "elected by the General Assembly."
            ),
            p(
                "At its first meeting after the election, the board of directors appoints, by "
                "resolution, a chairman, co-chairman, vice-chairman, secretary, treasurer and "
                "member by division of duties."
            ),
            p(
                "In the event of a vacancy in the main composition of the board of directors due "
                "to resignation or other reasons, it is imperative that replacement members be "
                "called to office in the order of the majority of votes received at the General "
                "Assembly."
            ),
            h3("Responsibilities and powers of the Board of Directors"),
            p("The board of directors fulfils the following tasks:"),
            ol([
                "Representing the Association, or authorising one of its members or a third party in this regard;",
                "Carrying out operations on income and expenditure accounts, preparing the budget for the next period and presenting it to the General Assembly;",
                "Preparing regulations on the activities of the Association and submitting them to the General Assembly for approval;",
                "With the authority granted by the General Assembly, acquiring real estate, selling movable and immovable property belonging to the Association, constructing buildings or structures, entering into leases, and establishing liens, mortgages or other rights in rem in favour of the Association;",
                "Ensuring that transactions regarding the opening of branches are carried out with the authority given by the General Assembly;",
                "Ensuring the inspection of the branches of the Association;",
                "Ensuring the opening of representative offices in places deemed necessary;",
                "Implementing the decisions taken at the General Assembly;",
                "Preparing the Association's operating account statements (or balance sheet and income statements), reporting on the activities of the board of directors at the end of each calendar year, and presenting these to the General Assembly when it meets;",
                "Ensuring the implementation of the budget;",
                "Deciding on the admission and removal of members from the Association;",
                "Taking and implementing all kinds of decisions within its authority in order to realise the purpose of the Association;",
                "Performing other duties using the powers given to the board by the legislation.",
            ]),
        ],
    ),
    (
        "section-11",
        "Establishment, duties and powers of the Audit Board",
        "Article 11.",
        [
            p(
                "The audit board, consisting of three main and three substitute members, is "
                "elected by the General Assembly."
            ),
            p(
                "If there is a vacancy in the primary membership of the audit board due to "
                "resignation or other reasons, it is mandatory to call the substitute members to "
                "duty in the order of the majority of votes received at the General Assembly."
            ),
            h3("Responsibilities and powers of the Audit Board"),
            p(
                "The audit board reviews the activities of the Association in accordance with the "
                "purpose and objectives set out in its Charter and with the procedures specified "
                "for the implementation of its tasks; it audits whether the books, accounts and "
                "records are maintained in accordance with the law and the Association's Charter "
                "and with the principles and procedures defined therein, with an audit frequency "
                "not exceeding one year, and reports the results of the inspection. The audit "
                "board presents its report to the board of directors and to the General Assembly "
                "at its meetings."
            ),
            p("The audit board may request a General Assembly meeting to be called when deemed necessary."),
        ],
    ),
    (
        "section-12",
        "Sources of income of the Association",
        "Article 12.",
        [
            p("The sources of income of the Association are as listed below:"),
            ol([
                "Membership dues: each member is charged an entrance fee of TRY 50 and monthly dues of TRY 50. These amounts may be increased or decreased only with the authorisation of the General Assembly.",
                "Branch / department dues: 50% of the member dues collected by the branches are sent to the headquarters every six months to cover the general expenses of the Association.",
                "Donations and aid made voluntarily by individuals and legal entities to the Association.",
                "Income obtained from activities such as tea and dinner meetings, trips and entertainment, performances, concerts and conferences organised by the Association.",
                "Income obtained from the assets of the Association.",
                "Donations and aid collected in accordance with the legislative provisions on aid collection.",
                "Profits obtained from commercial activities undertaken by the Association to provide the income needed to realise its purpose.",
                "Other income.",
            ]),
        ],
    ),
    (
        "section-13",
        "Bookkeeping principles and records to be kept",
        "Article 13.",
        [
            h3("Bookkeeping principles"),
            p(
                "The Association is required to maintain its books of accounts in accordance with "
                "established principles. However, if the annual gross income exceeds the limit "
                "specified in Article 31 of the Association Regulations, the books of accounts are "
                "kept on a balance-sheet basis starting from the next accounting period."
            ),
            p(
                "In case of switching to the balance-sheet method, if the specified limit falls "
                "below the limit for two consecutive accounting periods, the books may be "
                "converted back to the operating-account method from the following year."
            ),
            p(
                "Regardless of these restrictions, books of accounts may be maintained on a "
                "balance-sheet basis as determined by the board of directors."
            ),
            p(
                "If the Association opens a commercial enterprise, the accounting records of that "
                "commercial enterprise are maintained in accordance with the provisions of the "
                "Tax Procedure Law."
            ),
            h3("Registration procedure"),
            p(
                "The books and records of the Association are kept in accordance with the "
                "procedures and principles specified in the Association Regulations."
            ),
            h3("Books to keep and preserve"),
            p(
                "The Association holds the following books. (a) Books of accounts maintained on "
                "the basis of operating accounts, and the principles to be followed, are as "
                "follows:"
            ),
            ol([
                "Resolution Book: decisions of the board of directors are recorded in this book in order by date and number; all decisions are signed by the members present at the meeting.",
                "Member Registration Book: the personal details of those who join the Association as members and the dates of joining and leaving are recorded in this book; entry fees and annual dues paid by members are also recorded here.",
                "Document Registration Book: incoming and outgoing documents are recorded in this book with dates and serial numbers; originals of incoming and outgoing documents are filed; documents received or sent by e-mail are saved by printing them out.",
                "Business Accounts Book: income received and expenses incurred on behalf of the Association are clearly and regularly recorded in this book.",
            ]),
            p("(b) Books of accounts maintained on a balance-sheet basis, and the principles to be observed:"),
            p(
                "The books listed in items 1, 2 and 3 of paragraph (a) are also maintained in the "
                "case of accounting on a balance-sheet basis."
            ),
            p(
                "Ledger and General Ledger: the method of maintaining and recording these books "
                "follows the principles of the Tax Procedure Law and the General Communiqués on "
                "the Application of the Accounting System issued under the authority granted to "
                "the Ministry of Finance."
            ),
            h3("Certification of books"),
            p(
                "The books that the Association is required to keep (except the General Ledger) "
                "are certified by the Provincial Directorate of Civil Society Relations or by a "
                "notary public before being used. The use of these books continues until the "
                "pages run out, and there is no interim confirmation. However, the Journal Book "
                "kept on a balance-sheet basis must be re-certified every year in the last month "
                "before the year in which it will be used."
            ),
            h3("Preparation of the income statement and balance sheet"),
            p(
                "If records are kept on an operating-account basis, at year-end (31 December) a "
                "“Business Account Table” (specified in Appendix-16 of the Association "
                "Regulations) is prepared. If books are kept on a balance-sheet basis, a balance "
                "sheet and income statement are prepared at year-end (31 December) based on the "
                "Accounting System Application General Communiqués published by the Ministry of "
                "Finance."
            ),
        ],
    ),
    (
        "section-14",
        "Income and expenditure operations of the Association",
        "Article 14.",
        [
            h3("Income and expense documents"),
            p(
                "Association revenues are collected with a “Receipt Certificate” (an example is "
                "given in Appendix-17 of the Association Regulations). If the Association's "
                "revenues are collected through banks, documents such as receipts or account "
                "statements issued by the bank serve as receipts."
            ),
            p(
                "Association expenses are made with expense documents such as invoices, retail "
                "sale receipts and self-employment receipts. For payments within the scope of "
                "Article 94 of the Income Tax Law, an expense slip is required in accordance "
                "with the provisions of the Tax Procedure Law. For payments outside this scope, "
                "documents such as an “Expense Receipt” or “Bank Receipt” (examples in "
                "Appendix-13 of the Association Regulations) are used as expense documents."
            ),
            p(
                "Free deliveries of goods and services from the Association to individuals, "
                "institutions or organisations are made with the “In-Kind Aid Delivery Document” "
                "(an example is given in Appendix-14 of the Association Regulations)."
            ),
            p(
                "Free deliveries of goods and services made to the Association by individuals, "
                "institutions or organisations are accepted with the “In-Kind Donation Receipt "
                "Certificate” (an example is given in Appendix-15 of the Association Regulations)."
            ),
            p(
                "These documents are printed in the form and size shown in Appendix-13, -14 and "
                "-15, and held in binders of fifty self-carbonated originals plus fifty cover "
                "pages with sequential serial numbers, or in continuous form printed through "
                "electronic systems."
            ),
            h3("Receipts"),
            p(
                "“Receipt documents” (format and size specified in Appendix-17 of the Association "
                "Regulations) used in collecting Association income are printed at the printing "
                "house by decision of the board of directors."
            ),
            p(
                "The Association is responsible for matters relating to the printing and control "
                "of receipts, receiving them from the printing house, entering them in the "
                "ledger, transferring them between old and new treasurers, and ensuring their use "
                "by the person or persons authorised to collect income on behalf of the "
                "Association, in accordance with the relevant provisions of the Regulations."
            ),
            h3("Licence of authorisation"),
            p(
                "With the exception of the main members of the board of directors, the person or "
                "persons who will receive income on behalf of the Association are determined by a "
                "resolution of the board of directors, which also specifies the term of office. A "
                "“Certificate of Authorisation” (included in Schedule 19 of the Association "
                "Bylaws), containing the clear identity, signatures and photographs of the "
                "persons who will receive the income, is prepared by the Association in duplicate "
                "and approved by the chairman of the Association's board of directors. Main "
                "members of the board of directors can receive income without a power of attorney."
            ),
            h3("Retention period of income and expense documents"),
            p(
                "The validity period of authorisation certificates is determined by the board of "
                "directors for a maximum of one year. Expired permits are renewed in accordance "
                "with the first paragraph. In the event that a power of attorney expires, or the "
                "person to whom the power of attorney is issued resigns, dies or is removed from "
                "office, the issued powers of attorney must be submitted to the Association board "
                "within one week. The authority to collect revenue may also be revoked at any "
                "time by decision of the board of directors."
            ),
            p(
                "With the exception of the books, the receipts, expense documents and other "
                "records held by the Association shall be retained — without prejudice to the "
                "periods specified in special laws — for five years, in the order of the number "
                "and date entries in the books in which they are recorded."
            ),
        ],
    ),
    (
        "section-15",
        "Submission of the annual declaration",
        "Article 15.",
        [
            p(
                "The activities of the Association, together with the income and expenses of the "
                "previous year, after approval by the board of directors, are recorded in the "
                "“Declaration of the Association” on the results of transactions at the end of "
                "the year (presented in Appendix-21 of the Association Regulations). This "
                "Declaration is transferred by the chairman of the Association to the appropriate "
                "local body authorities during the first four months of each calendar year."
            ),
        ],
    ),
    (
        "section-16",
        "Notification obligations",
        "Article 16.",
        [
            h3("Notifications to civil authorities"),
            p(
                "Notification of the results of the General Assembly: within thirty days after "
                "the regular or extraordinary meeting of the General Assembly, notification of "
                "the results — including the main and alternate members elected to the board, the "
                "audit council and other bodies (Appendix-3 of the Association Regulations) — "
                "shall be submitted to local authorities. In case of a change of the Charter at "
                "the General Assembly, the minutes of the General Assembly, the old and new forms "
                "of the amended articles, and the final version of the Association's charter — "
                "each page signed by the absolute majority of the members of the board of "
                "directors — are submitted to the local government body within the period "
                "specified in this paragraph."
            ),
            h3("Real-estate notification"),
            p(
                "Real estate acquired by the Association is reported to the local administrative "
                "authority by completing a “Real Estate Declaration” (Appendix-26 of the "
                "Association Regulations) within thirty days from the date of registration in the "
                "land registry."
            ),
            h3("Notification of receipt of financial assistance from overseas"),
            p(
                "If the Association is to receive assistance from abroad, it must complete the "
                "“Notification of Receipt of Assistance from Overseas” (Appendix-4 of the "
                "Association Regulations) and notify the local authority before receiving the "
                "assistance. Cash assistance must be obtained through banks and notification "
                "requirements must be met before use."
            ),
            h3("Notification of changes"),
            p(
                "A change of location of the Association (Appendix-24) — “Notice of change of "
                "location” — and any changes occurring in the bodies of the Association except "
                "the General Assembly, are notified to the local authority within thirty days of "
                "the change by filing the “Notifications of changes in the association's bodies” "
                "(Appendix-25)."
            ),
            p(
                "Changes made to the Association's charter are also communicated to the local "
                "authority within thirty days of the General Assembly at which the charter was "
                "amended, as an attachment to the notice of the results of the General Assembly "
                "meeting."
            ),
        ],
    ),
    (
        "section-17",
        "Internal audit of the Association",
        "Article 17.",
        [
            p(
                "Just as an internal audit may be carried out by the General Assembly, the board "
                "of directors or the audit board of the Association, audits may also be carried "
                "out by independent audit organisations. The fact that the audit is conducted by "
                "the General Assembly, the board of directors or independent audit firms does not "
                "relieve the audit body from liability."
            ),
        ],
    ),
    (
        "section-18",
        "Rules for borrowing by the Association",
        "Article 18.",
        [
            p(
                "The Association may borrow money by decision of the board of directors when "
                "necessary to achieve its purpose and carry out its activities. This borrowing "
                "may be made by purchasing goods and services on credit, or in cash. However, "
                "this borrowing cannot be made in amounts that cannot be covered by the "
                "Association's income resources, or in a manner that would cause the Association "
                "to have payment difficulties."
            ),
        ],
    ),
    (
        "section-19",
        "Establishment of branches of the Association",
        "Article 19.",
        [
            p(
                "The Association may open branches in places deemed necessary by decision of the "
                "General Assembly. For this purpose, a board of founders of at least three people "
                "authorised by the board of directors of the Association submits the branch "
                "establishment notification and the necessary documents specified in the "
                "Association Regulations to the highest administrative authority of the place "
                "where the branch will be opened."
            ),
        ],
    ),
    (
        "section-20",
        "Responsibilities and powers of the branches",
        "Article 20.",
        [
            p(
                "Branches are internal organisations of the Association that do not have a legal "
                "entity, that are entrusted and authorised to carry out autonomous activities in "
                "line with the objectives and service subjects of the Association, and that are "
                "responsible for all receivables and debts arising from all transactions."
            ),
        ],
    ),
    (
        "section-21",
        "Bodies of branches and applicable provisions",
        "Article 21.",
        [
            p(
                "The organs of a branch are its general assembly, board of directors and audit "
                "board. The general assembly is composed of the registered members of the branch. "
                "The board of directors is elected by the general assembly of the branch — five "
                "main and five substitute members — as well as the audit board of three main and "
                "three substitute members."
            ),
            p(
                "The responsibilities and powers of these bodies, and other matters related to "
                "the Association included in this Charter, are also applied within the branch in "
                "the framework stipulated by the legislation."
            ),
        ],
    ),
    (
        "section-22",
        "Time of branch general meetings and representation at headquarters",
        "Article 22.",
        [
            p(
                "Branches must conclude their ordinary general assembly meetings at least two "
                "months before the headquarters' General Assembly meeting. The ordinary general "
                "assembly meetings of the branches meet every three years, in January, on the "
                "day, place and time determined by the branch board of directors. Branches are "
                "obliged to submit a copy of the general meeting results notification to the "
                "local administrative authority and to the headquarters of the Association "
                "within thirty days following the date of the meeting."
            ),
            p(
                "If the number of branches is three or less, then all their members have the "
                "right to participate directly in the General Assembly meeting of the "
                "Association. When the number of branches is more than three, one (1) delegate "
                "for every twenty (20) members registered in the branch — and one further "
                "delegate from among the remaining members if more than ten remain — has the "
                "right to participate in the General Assembly meeting of the Association, "
                "elected at the branch general assembly meetings."
            ),
            p(
                "Delegates elected at the last branch general assembly are present at the "
                "General Assembly meeting of the Association. Members of the headquarters board "
                "of directors and audit board attend the headquarters General Assembly, but "
                "cannot vote unless they are elected as delegates on behalf of a branch."
            ),
            p(
                "Members of the board of directors or audit board of a branch leave their "
                "positions in the branch upon election to the board of directors or audit board "
                "of the head office."
            ),
        ],
    ),
    (
        "section-23",
        "Opening of representative offices",
        "Article 23.",
        [
            p(
                "The Association may, by decision of the board of directors, open representative "
                "offices in places that it considers necessary for the implementation of its "
                "activities. The address of the representative office is communicated in writing "
                "to the local administrative authority of that place by the person or persons "
                "appointed as representatives by decision of the board of directors. "
                "Representatives may not be represented in the General Assembly. Branches "
                "cannot open representative offices."
            ),
        ],
    ),
    (
        "section-24",
        "Amendments to the Charter",
        "Article 24.",
        [
            p("Changes to the Charter may be made by decision of the General Assembly."),
            p(
                "In order to make changes to the Charter at the General Assembly, a two-thirds "
                "majority of the members entitled to attend and vote in the General Assembly is "
                "required. If the meeting is postponed due to lack of majority, no majority is "
                "required at the second meeting; however, the number of members attending this "
                "meeting cannot be less than twice the total number of members of the board of "
                "directors and the audit board combined."
            ),
            p(
                "The majority decision required for a Charter change is two thirds of the votes "
                "of the members present at the meeting and entitled to vote. Voting for Charter "
                "amendments is carried out openly at the General Assembly."
            ),
        ],
    ),
    (
        "section-25",
        "Dissolution of the Association and liquidation of assets",
        "Article 25.",
        [
            p("The General Assembly may decide to terminate the Association at any time."),
            p(
                "To discuss the issue of termination at the General Assembly, a majority of two "
                "thirds of the members entitled to attend and vote in the General Assembly is "
                "required. If the meeting is postponed due to lack of majority, no majority is "
                "required at the second meeting; however, the number of members attending this "
                "meeting cannot be less than twice the total number of members of the board of "
                "directors and the audit board combined."
            ),
            p(
                "The majority required for a termination decision is two thirds of the votes of "
                "the members who attend the meeting and have the right to vote. Voting on the "
                "termination decision is carried out openly at the General Assembly."
            ),
            h3("Liquidation procedures"),
            p(
                "When a decision is made to terminate the Association at the General Assembly, "
                "the money, property and rights of the Association are liquidated by a "
                "liquidation commission consisting of the last board members. These procedures "
                "begin from the date on which the General Assembly decided on termination, or "
                "the date of automatic termination. The phrase “The World Association of "
                "Azerbaijani Scientists in Liquidation” is used in the name of the Association "
                "in all transactions during the liquidation period."
            ),
            p(
                "The liquidation commission is responsible and authorised to complete the "
                "liquidation of the funds, property and rights of the Association from beginning "
                "to end in accordance with the law. The commission first reviews the "
                "Association's records, identifying the books, receipts, supplies, titles, bank "
                "statements and other documents belonging to the Association, and recording its "
                "assets and liabilities. During the liquidation process, the creditors of the "
                "Association are approached and the Association's assets, if any, are converted "
                "into cash and paid to the creditors."
            ),
            p(
                "If the Association is a creditor, the receivables are collected. All money, "
                "property and rights remaining after collection of receivables and repayment of "
                "debts are transferred to a place determined at the General Assembly. If the "
                "place of transfer is not determined by the General Assembly, the assets are "
                "transferred to the association closest to the Association's purpose in the "
                "province where the Association is located, and which has the largest number of "
                "members on the date of termination."
            ),
            p(
                "All transactions related to liquidation are reflected in the liquidation "
                "report, and liquidation procedures are completed within three months — except "
                "for additional periods granted by local administrative authorities for good "
                "reason."
            ),
            p(
                "After the liquidation is completed and the money, property and rights of the "
                "Association are transferred, the liquidation commission must, within seven "
                "days, notify the local government of the location of the Association's "
                "headquarters by letter, with a report on the liquidation attached."
            ),
            p(
                "The final members of the board of directors are responsible for maintaining "
                "the books and records of the Association as a liquidation committee. This "
                "responsibility may also be assigned to a member of the board of directors. "
                "These books and records must be kept for five years."
            ),
        ],
    ),
    (
        "section-26",
        "Absence of provision",
        "Article 26.",
        [
            p(
                "In matters not specified in this Charter, the provisions of the Associations "
                "Law, the Turkish Civil Code, the Association Regulations issued with reference "
                "to these laws, and other relevant legislation regarding associations shall apply."
            ),
            p(
                "Provisional Article 1 — Until the bodies of the Association are established at "
                "the first General Assembly, the temporary board members listed below will "
                "represent the Association and carry out the affairs and transactions related "
                "to it."
            ),
        ],
    ),
]


def render_section(anchor_id: str, title: str, article_label: str, blocks: list[str]) -> str:
    parts = [
        f'<section class="charter-card" id="{anchor_id}">',
        f'<div class="article-separate-title">{h(title, quote=False)}</div>',
        '<div class="section-head">',
        '<span class="icon">📜</span>',
        f"<h2>{h(article_label, quote=False)}</h2>",
        "</div>",
        '<div class="charter-body">',
        *blocks,
        "</div>",
        "</section>",
    ]
    return "\n".join(parts)


def build_stack() -> str:
    return "\n".join(
        render_section(*section) for section in SECTIONS
    )


def main() -> None:
    path = ROOT / "en" / "charter.html"
    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r'(<div class="charter-stack">)(.*?)(</div>\s*</div>\s*</main>)',
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise SystemExit("Could not locate <div class=\"charter-stack\"> block in en/charter.html")

    new_stack = "\n" + build_stack() + "\n"
    updated = text[: match.start(2)] + new_stack + text[match.end(2):]

    if updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Updated en/charter.html — replaced {len(SECTIONS)} sections.")
    else:
        print("No changes.")


if __name__ == "__main__":
    main()
