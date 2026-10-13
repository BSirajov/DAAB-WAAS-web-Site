# -*- coding: utf-8 -*-
"""Full CV-voice profile rewrites for entries that were truncated in the first pass."""
from __future__ import annotations

# Facts taken only from existing CV content; meta voice removed.
PROFILE_FIXES: dict[str, str] = {
    "Aliyev_Ismayil_CV_EN.docx": (
        "Ismayil Aliyev is a professor at St. Petersburg State University of Economics, in the Department of "
        "Economics and Management of Enterprises and Industrial Complexes, a post he has held since 2023. He "
        "graduated in labor economics in 1992 from St. Petersburg State University of Economics and Finance, "
        "later received the Candidate of Economic Sciences degree, and in 2007 defended a doctoral dissertation "
        "on incomes and living standards in the context of improving the social policy of the Russian Federation. "
        "He received the associate-professor title in 2002 and the professor title in 2009. His record includes "
        "more than 150 publications, among them 12 textbooks and monographs, and supervision of 10 candidates of "
        "sciences and 2 doctors of sciences."
    ),
    "Aliyev_Ramin_CV_EN.docx": (
        "Ramin Aliyev is a professor of guidance and psychological counseling at Hasan Kalyoncu University in "
        "Gaziantep. He was appointed professor on 27 March 2024, having served as associate professor there from "
        "23 January 2019. He received a doctorate in educational psychology from Ankara University on 27 January "
        "2011, a master’s degree in the same field on 1 September 2004, and a bachelor’s degree in guidance and "
        "psychological counseling on 18 July 2001."
    ),
    "Atakishiyev_Natig_CV_EN.docx": (
        "Natig Atakishiyev is a researcher, with the rank Investigador Nacional Emérito, at the Institute of "
        "Mathematics of the National Autonomous University of Mexico in Cuernavaca, where he has worked since 1996. "
        "He received an MSc-equivalent diploma from Azerbaijan State University in 1961, a PhD-equivalent Candidate "
        "of Physical and Mathematical Sciences degree from the Institute of High Energy Physics in Serpukhov in 1971, "
        "and the Doctor of Physical and Mathematical Sciences degree from the Institute of Theoretical Physics in "
        "Kiev in 1987. From 1983 to 1994 he headed the Laboratory for the Theory of Elementary Particles at the "
        "Institute of Physics in Baku. His record includes 131 journal papers and 62 conference papers, with 2,825 "
        "citations and an h-index of 28."
    ),
    "Efendiyev_Messoud_CV_EN.docx": (
        "Messoud Efendiyev is rector’s distinguished visiting professor at Marmara University in Istanbul and head "
        "of the Department of Dynamical Systems at Helmholtz Zentrum München, with a guest and leading professorship "
        "linked to the Technical University of Munich. He received a PhD from Lomonosov Moscow State University in "
        "1980 and a Dr. Sci. (habilitation) from the Free University of Berlin in 1998. He is the author of 8 books "
        "and an author or coauthor of 186 journal and conference papers. His research interests include "
        "infinite-dimensional dynamical systems, mathematical biology and medicine, and nonlinear equations of "
        "mathematical physics."
    ),
    "Gayibli_Khagani_CV_EN.docx": (
        "Khagani Gayibli is director of the Turkish Language Center at the University of Tartu, a post he has held "
        "since 1998. He received a PhD in history from the University of Tartu in 2008–2011 and an MA in Uralic "
        "languages there in 2003–2005. He has been chair of the Estonia-Azerbaijan Society since 1994 and a member "
        "and deputy chair of the board of the Congress of World Azerbaijanis since 2001. His publications include "
        "books of essays, poetry, and Turkish-Estonian language guides, as well as translations from Azerbaijani, "
        "Estonian, and Turkish. He was awarded the Taraggi Medal on 21 April 2022."
    ),
    "Gojayev_Zahid_CV_EN.docx": (
        "Zahid Gojayev is deputy director for innovation and implementation at the Federal Scientific Agroengineering "
        "Center VIM and a professor at Moscow Polytechnic University and Bauman Moscow State Technical University. "
        "He is a Doctor of Technical Sciences and a corresponding member of the Russian Academy of Sciences, elected "
        "in 2019. He defended a Candidate of Technical Sciences dissertation at Bauman Moscow State Technical "
        "University in 1979 and a Doctor of Technical Sciences dissertation in 1994. From 2002 to 2014 he was "
        "general director of the Federal Research and Testing Center for Mechanical Engineering. His record includes "
        "more than 300 scientific works, monographs, and patents."
    ),
    "Guliyev_Arif_CV_EN.docx": (
        "Arif Guliyev is a professor in the Department of Constitutional Law, International Law and Public-Law "
        "Subjects at the Kyiv University of Intellectual Property and Law of the National University Odesa Law "
        "Academy, and a member of its scientific council since 2021. In 2005 he received the Candidate of Sciences "
        "degree in public administration at the Academy of Public Administration under the President of Ukraine "
        "(recognized in Azerbaijan as Candidate of Legal Sciences). In 2012 he received the Doctor of Legal Sciences "
        "degree at the Institute of Legislation of the Verkhovna Rada of Ukraine. His record includes 8 monographs, "
        "3 textbooks, 2 teaching aids, more than 250 articles, including 3 Scopus articles, and supervision of "
        "25 candidates and 2 doctors of legal sciences."
    ),
    "Guliyeva_Aynur_CV_EN.docx": (
        "Aynur Guliyeva is an associate professor at the University of Technology Tarbes Occitanie Pyrénées, where "
        "she has worked since January 2024. She received a PhD in chemistry of materials from the University of "
        "Orléans in 2016–2019, a Master 2 in polymers for advanced technologies from the University of Grenoble "
        "Alpes in 2015–2016, and a bachelor’s degree in chemistry from Baku State University in 2010–2014. She was "
        "a scientist at Lonza Capsugel in Colmar, a research engineer at PIMM, ENSAM in Paris, and a postdoctoral "
        "researcher at the University of Delaware. She has published 8 articles."
    ),
    "Mammadov_Agamali_CV_EN.docx": (
        "Agamali Mammadov is professor and head of the Department of Sociology of Communication Systems at the "
        "Faculty of Sociology of Lomonosov Moscow State University, where he has worked since September 2009. He "
        "graduated with honors from the Faculty of Philosophy of the same university in 1980, with a qualification "
        "in sociology, and also holds a qualification in law. He received the Doctor of Sociological Sciences "
        "degree in 1998 and the title of professor in 2000. His record includes an h-index of 44, more than 52 "
        "monographs and textbooks, and supervision of 25 candidates of sciences and 3 doctors of sciences."
    ),
    "Mammadov_Nizami_CV_EN.docx": (
        "Nizami Mammadov is a professor at the Russian Presidential Academy of National Economy and Public "
        "Administration in Moscow, where he has worked since 1995. He studied automation and computer engineering "
        "at the Azerbaijan Polytechnic Institute (1962–1967), received the Candidate of Philosophical Sciences "
        "degree in 1975, and defended a doctoral thesis at the Institute of Philosophy of the USSR Academy of "
        "Sciences in 1984. The Higher Attestation Commission of the USSR awarded him the title of professor in "
        "1988. His record includes 400 publications, an h-index of 33, and preparation of 41 candidates and "
        "doctors of sciences."
    ),
    "Masumova_Nigar_CV_EN.docx": (
        "Nigar Masumova is an associate professor in the Department of World Economy at MGIMO University in Moscow, "
        "head of the Department of Advertising and Public Relations, and deputy dean of the School of International "
        "Journalism. She received a PhD in economics at MGIMO in May 2012 and a specialist diploma in foreign "
        "economic relations there in June 2007. Her research interests include the social and economic development "
        "of Turkey and Iran, and branding. Her main works include a 2015 book on Turkey and contributions connected "
        "with volumes edited by A. Bulatov."
    ),
    "Mehdiyev_Gafar_CV_EN.docx": (
        "Gafar Mehdiyev is a professor at Erciyes University in Kayseri, in the Department of Armenian Language and "
        "Culture, a title he has held since 2016. He has been a faculty member there since 2010. He graduated from "
        "the Faculty of Journalism of Baku State University in 1980 and received a PhD in political sciences in "
        "2007 for a dissertation on the role of the press in bringing out facts about the Armenian question, based "
        "on Armenian and Turkish press materials. He worked as a journalist and editor in Baku from 1980 to 2017 "
        "and taught at Baku State University from 2004 to 2012. His record includes more than 100 articles and "
        "about 20 books."
    ),
    "Mehmedov_Emirullah_CV_EN.docx": (
        "Emirullah Mehmedov is an emeritus professor and leading researcher at the Nanotechnology Research Center "
        "of Bilkent University, where he has worked since 2011. Publications use the name Amirullah M. Mamedov. He "
        "received a PhD in physics and mathematics from the Ioffe Institute in 1973 for a thesis on the optical and "
        "electro-optical properties of photoferroelectric materials, carried out at the Vavilov State Optical "
        "Institute. He received the Doctor of Sciences in physics and mathematics in 1982 from the regional council "
        "in Riga, and the title of full professor of optics in 1988. His record includes more than 350 publications. "
        "He was scientific advisor to ASELSAN in 1992–2006."
    ),
    "Najafoglu_Hajali_CV_EN.docx": (
        "Hajali Najafoglu is professor of inorganic chemistry at Kafkas University. He earned a doctorate in "
        "inorganic chemistry from the Azerbaijan Academy of Sciences and a master’s degree in organic chemistry "
        "and a first degree in chemistry from Azerbaijan State University. He was an assistant professor at Kafkas "
        "University in 1992–1995, an associate professor in 1995–1998, and a professor from 1998. Publications "
        "from the 1970s use the name G. N. Nadzhafov."
    ),
    "Rzayev_Teymur_CV_EN.docx": (
        "Teymur Rzayev is a professor in the Department of Plastic Arts at Yeditepe University. He received a "
        "doctorate from Azerbaijan State University of Fine Arts in 2009 for the thesis Pagan Sculpture of "
        "Azerbaijan, supervised by Telman Ibrahimov. His master’s thesis, Smena, was completed in 1988 at the "
        "Azerbaijan State Academy of Artists under Mikail Abdullayev. He has taught at Yeditepe University since "
        "2006, as a lecturer until 2012 and as a doctoral lecturer in 2012–2014, and later held associate-professor "
        "and professor ranks."
    ),
    "Sultansoy_Saleh_CV_EN.docx": (
        "Saleh Sultansoy is a professor at TOBB University of Economics and Technology in Ankara, where he has "
        "worked since 2007, and a leading researcher at the Institute of Physics of the Azerbaijan National Academy "
        "of Sciences since 1993. He studied at Azerbaijan State University from 1969 to 1974 and received a "
        "doctorate in 1985 at the Institute of High Energy Physics in Serpukhov. His fields include high-energy "
        "physics, particle accelerators and their applications, science and technology strategy, and the history of "
        "science. His record includes more than 800 scientific publications, of which 632 are in Science Citation "
        "Index journals."
    ),
    "Zeynalova_Khadija_CV_EN.docx": (
        "Khadija Zeynalova is an associate professor at the Detmold University of Music and artistic director of "
        "the Bridge of Sound orchestra and of the Harmony of Sound festival, which she founded in Germany. She "
        "studied music theory at Sumgayit Music College (1990–1994) and composition and musicology at the Baku "
        "Music Academy (1994–2000), and continued composition studies in Detmold in 2005–2006. From 2006 to 2012 "
        "she was a doctoral student at the University of Paderborn; her thesis addresses Azerbaijani musical "
        "culture of the 20th century and tendencies in Western music. From 2000 to 2005 she taught as an associate "
        "professor at the Azerbaijan State University of Culture and Arts. Her record includes more than 40 books, "
        "works, and textbooks."
    ),
    "Abdullayev_Rauf_CV_EN.docx": (
        "Rauf Abdullayev is a database software administrator at proCtec GmbH in Aachen, where he has worked since "
        "January 2023. He holds a bachelor’s degree in computer engineering from the University of Duisburg-Essen "
        "(2015–2022); his thesis project was ManageData, a mobile application in Xamarin. From April 2015 to "
        "January 2023 he worked in front-office and IT support at Novum Hospitality AG in Düsseldorf, and in 2016 "
        "he completed an SQL database internship at Karttel GmbH in Neuss. Earlier study and teaching-assistant "
        "work includes posts in Strasbourg and Baku."
    ),
    "Asgerova_Sevinj_CV_EN.docx": (
        "Sevinj Asgerova is a professor and chief researcher at the N. I. Pirogov Russian National Research Medical "
        "University in Moscow. Her specialty is physician and ophthalmologist-surgeon. She defended a doctoral "
        "dissertation in 2005 at the S. N. Fyodorov Eye Microsurgery complex in Moscow. She is the author of 18 "
        "invention patents, 15 rationalization proposals, and more than 140 scientific articles and abstracts. Her "
        "honors include gold medals of Hippocrates and V. I. Vernadsky and the title Honored Worker of Science and "
        "Education."
    ),
}
