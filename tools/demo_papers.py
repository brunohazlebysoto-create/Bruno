"""Demo papers in pediatric surgery for pipeline testing without external API access."""

# ── Apendicitis aguda pediátrica ──────────────────────────────────────────── #
APPENDICITIS = [
    {
        "pmid": "36112345",
        "title": "Laparoscopic versus open appendectomy in children: a systematic review and meta-analysis of 25,000 patients",
        "authors": ["St Peter SD", "Adibe OO", "Iqbal CW", "Fike FB"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2023",
        "abstract": "Background: Laparoscopic appendectomy (LA) has become standard in adult surgery, but its superiority in children remains debated. We conducted a systematic review of 38 RCTs and cohort studies (n=25,412, ages 1–18 years). Methods: Primary outcomes were wound infection, intra-abdominal abscess, operative time, and length of stay. Results: LA significantly reduced wound infection (OR 0.31, 95% CI 0.22–0.44, p<0.001) and length of stay (MD −0.8 days, 95% CI −1.1 to −0.5). Intra-abdominal abscess was similar (OR 1.12, 95% CI 0.87–1.44). Operative time was longer with LA (+8.2 min). For perforated appendicitis, LA reduced wound infections further (OR 0.24). Conclusions: LA should be the preferred approach for pediatric appendicitis, including perforated cases, in experienced hands.",
        "doi": "10.1016/j.jpedsurg.2023.01.001",
        "citations": 287,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36112345/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
    {
        "pmid": "36223456",
        "title": "Non-operative management of uncomplicated appendicitis in children: APPAC-Pediatric RCT",
        "authors": ["Minneci PC", "Hade EM", "Lawrence AE", "Sebastião YV"],
        "journal": "JAMA",
        "year": "2023",
        "abstract": "Importance: Non-operative management (NOM) with antibiotics has emerged as an alternative to appendectomy in uncomplicated appendicitis. In this RCT of 990 children (ages 7–17), NOM with 10-day antibiotic course (amoxicillin-clavulanate) was compared with appendectomy. Results: NOM avoided surgery in 67.1% at 1 year. Treatment success (no significant disability) was 78.8% NOM vs 88.1% appendectomy (difference −9.3%, 95% CI −14.3 to −4.3). Complications were higher with failed NOM. Healthcare utilization was lower with successful NOM. Conclusion: NOM is a reasonable option for selected children with uncomplicated appendicitis, though rates of disability were higher. Shared decision-making is essential.",
        "doi": "10.1001/jama.2023.2912",
        "citations": 412,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36223456/",
        "publication_types": ["Randomized Controlled Trial"],
    },
    {
        "pmid": "36334567",
        "title": "Scoring systems for pediatric appendicitis: validation of PAS, AIR, and Alvarado scores",
        "authors": ["Bachur RG", "Callahan MJ", "Monuteaux MC"],
        "journal": "Annals of Emergency Medicine",
        "year": "2022",
        "abstract": "Prospective validation of Pediatric Appendicitis Score (PAS), Appendicitis Inflammatory Response (AIR) and Alvarado scores in 2,625 children ≤18 years presenting with abdominal pain. PAS ≥6: sensitivity 90%, specificity 73%, AUC 0.88. AIR ≥5: sensitivity 87%, specificity 79%, AUC 0.90. Alvarado ≥7: sensitivity 72%, specificity 82%, AUC 0.84. Ultrasound added diagnostic value when scores were intermediate (4–7). CT should be reserved for indeterminate cases after ultrasound. Conclusion: PAS and AIR outperform Alvarado; an imaging-first strategy with ultrasound reduces CT use without increasing negative appendectomy rates.",
        "doi": "10.1016/j.annemergmed.2022.03.015",
        "citations": 198,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36334567/",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "35998765",
        "title": "Enhanced recovery after surgery (ERAS) protocol for pediatric appendectomy: prospective cohort",
        "authors": ["Pearce G", "Casey L", "Nair R"],
        "journal": "Pediatric Surgery International",
        "year": "2022",
        "abstract": "ERAS protocol implemented in 312 children undergoing appendectomy (laparoscopic 89%). Components: preoperative carbohydrate loading, multimodal analgesia (ketorolac 0.5 mg/kg + paracetamol), early oral intake (4 hours post-op), same-day mobilization. Results: Length of stay reduced from 2.8 to 1.4 days (p<0.001). Opioid use decreased by 62%. Complication rate was unchanged (8.3% vs 7.9%). Patient satisfaction improved. ERAS was safe and effective for pediatric appendectomy.",
        "doi": "10.1007/s00383-022-05101-4",
        "citations": 89,
        "source": "CrossRef",
        "url": "https://doi.org/10.1007/s00383-022-05101-4",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "35887654",
        "title": "Timing of appendectomy and outcomes in perforated appendicitis in children",
        "authors": ["Kim HJ", "Lee JH", "Park JY"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2022",
        "abstract": "Retrospective cohort of 1,847 children with perforated appendicitis. Early appendectomy (<12 hours of presentation) vs interval appendectomy after 6–8 weeks of antibiotic treatment. Early appendectomy group: shorter total hospital stay (8.2 vs 12.4 days, p<0.001), lower failure rate (3% vs 18%), similar complication rates. Interval appendectomy had 18% failure rate requiring emergency surgery. Conclusion: Early appendectomy for perforated appendicitis is associated with better outcomes and should be preferred over interval approach in children.",
        "doi": "10.1016/j.jpedsurg.2022.02.009",
        "citations": 134,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/35887654/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Invaginación intestinal ───────────────────────────────────────────────── #
INTUSSUSCEPTION = [
    {
        "pmid": "36445678",
        "title": "Pneumatic versus hydrostatic reduction of intussusception in children: systematic review",
        "authors": ["Applegate KE", "Anderson JM", "Klatte EC"],
        "journal": "Radiology",
        "year": "2023",
        "abstract": "Systematic review of 28 studies (n=6,412 children) comparing pneumatic (air/CO2) vs hydrostatic (water/barium/saline) enema reduction of intussusception. Pneumatic reduction had higher success rate (85% vs 76%, OR 1.72, 95% CI 1.34–2.21, p<0.001) and lower perforation risk (0.14% vs 0.43%). Fluoroscopic guidance with pressure limit ≤120 mmHg and ≤3 attempts was safe. Ultrasound-guided hydrostatic reduction success rate was comparable to fluoroscopic pneumatic (83%). Conclusion: Pneumatic reduction is preferred as first-line; ultrasound-guided hydrostatic is a valid radiation-free alternative.",
        "doi": "10.1148/radiol.220234",
        "citations": 156,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36445678/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
    {
        "pmid": "36556789",
        "title": "Ultrasound-guided saline enema reduction of intussusception: prospective study in 500 children",
        "authors": ["Yoon CH", "Kim HJ", "Goo HW"],
        "journal": "American Journal of Roentgenology",
        "year": "2022",
        "abstract": "Prospective study of 500 children (median age 14 months) with intussusception confirmed by ultrasound. Saline enema under ultrasound guidance: success rate 91.2% (456/500). Recurrence at 24 hours: 8.7%. Perforation rate: 0.2%. No radiation exposure. Average reduction time: 12 minutes. Risk factors for failure: prolonged duration >24 hours (OR 4.2), lead point (OR 8.9), age <3 months. Repeat enema on recurrence successful in 85%. Conclusion: US-guided saline enema is highly effective, safe, and eliminates radiation exposure.",
        "doi": "10.2214/AJR.22.27850",
        "citations": 203,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36556789/",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "35776890",
        "title": "Surgical management of irreducible intussusception in children: laparoscopic versus open approach",
        "authors": ["Bonnard A", "Zamakhshary M", "Bass J"],
        "journal": "Pediatric Surgery International",
        "year": "2022",
        "abstract": "Retrospective multicenter study of 287 children requiring surgical reduction after failed enema. Laparoscopic (n=142) vs open (n=145) manual reduction. Laparoscopic group: shorter operative time (38 vs 52 min), less postoperative pain, shorter hospital stay (2.1 vs 3.4 days). Conversion rate 9.2%. Bowel resection required in 18% (similar both groups). Complication rate 12% vs 16%. Conclusion: Laparoscopic approach is safe and feasible for surgical management of intussusception; bowel resection rates are similar.",
        "doi": "10.1007/s00383-022-05061-7",
        "citations": 67,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/35776890/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Estenosis hipertrófica del píloro ─────────────────────────────────────── #
PYLORIC_STENOSIS = [
    {
        "pmid": "36667890",
        "title": "Laparoscopic versus open Ramstedt pyloromyotomy: meta-analysis of 8,000 infants",
        "authors": ["Hall NJ", "Ade-Ajayi N", "Al-Zubaidy F"],
        "journal": "Annals of Surgery",
        "year": "2023",
        "abstract": "Meta-analysis of 32 studies (n=8,234 infants) comparing laparoscopic (LP) vs open (OP) pyloromyotomy. LP: significantly lower incidence of mucosal perforation (OR 0.61, 95% CI 0.42–0.88), shorter time to full feeds (MD −6.2 hours, 95% CI −9.1 to −3.3), shorter hospital stay (MD −0.5 days, 95% CI −0.7 to −0.2), better cosmetic outcome. Operative time and incomplete pyloromyotomy rates were similar. Conclusion: LP is preferred for infantile hypertrophic pyloric stenosis in centers with appropriate laparoscopic expertise.",
        "doi": "10.1097/SLA.0000000000005234",
        "citations": 178,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36667890/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
    {
        "pmid": "36778901",
        "title": "Preoperative optimization in hypertrophic pyloric stenosis: bicarbonate threshold and safe anesthesia",
        "authors": ["Carpenter TC", "Shann F", "Waisman D"],
        "journal": "Pediatric Anesthesia",
        "year": "2023",
        "abstract": "Retrospective analysis of 1,156 infants with hypertrophic pyloric stenosis (HPS). Pre-operative serum bicarbonate ≥30 mEq/L correlated with higher risk of post-extubation apnea (OR 4.1, p<0.001). Proposed threshold for safe surgery: bicarbonate ≤26 mEq/L, chloride ≥90 mEq/L, pH ≤7.45. Median resuscitation time 18 hours. Normal saline with KCl supplementation achieved correction in 94%. Regional blocks (RSB) reduced opioid requirements by 68%. Conclusion: Metabolic alkalosis must be fully corrected before pyloromyotomy; serum bicarbonate ≤26 mEq/L is a safe threshold.",
        "doi": "10.1111/pan.14623",
        "citations": 134,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36778901/",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "35889012",
        "title": "Ultrasound diagnosis of hypertrophic pyloric stenosis: diagnostic accuracy in 2,400 infants",
        "authors": ["Naffaa L", "Rottem S", "Cohen M"],
        "journal": "Journal of Ultrasound in Medicine",
        "year": "2022",
        "abstract": "Prospective multicenter study evaluating ultrasound (US) criteria for HPS in 2,412 infants (mean age 5.2 weeks). Muscle wall thickness ≥3 mm and channel length ≥15 mm had sensitivity 98.7%, specificity 99.3%, PPV 99.1%. Single-operator US: sensitivity 96.2%. Pyloric volume >1.4 cm³ added diagnostic value. US eliminated barium study need in 96%. Conclusion: US is the gold-standard diagnostic tool for HPS with near-perfect accuracy when diagnostic criteria are strictly applied.",
        "doi": "10.1002/jum.15723",
        "citations": 89,
        "source": "CrossRef",
        "url": "https://doi.org/10.1002/jum.15723",
        "publication_types": ["Cohort Study"],
    },
]

# ── Enfermedad de Hirschsprung ────────────────────────────────────────────── #
HIRSCHSPRUNG = [
    {
        "pmid": "36990123",
        "title": "Transanal endorectal pull-through for Hirschsprung disease: systematic review of long-term outcomes",
        "authors": ["Langer JC", "Rollins MD", "Levitt M"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2023",
        "abstract": "Systematic review of 42 studies (n=3,876 patients) evaluating transanal endorectal pull-through (TEPT) for Hirschsprung disease (HD). TEPT vs laparoscopic-assisted pull-through (LAPT): similar continence rates at 5 years (82% vs 84%), similar enterocolitis rates (28% vs 27%). TEPT shorter operative time (98 vs 142 min). Long-segment HD had worse outcomes regardless of technique. Soiling at 5 years: 18% TEPT vs 15% LAPT (p=0.21). Conclusion: TEPT remains standard for short-segment HD; LAPT preferred for long-segment or difficult anatomy. Both show equivalent long-term functional outcomes.",
        "doi": "10.1016/j.jpedsurg.2023.03.002",
        "citations": 211,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36990123/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
    {
        "pmid": "36101234",
        "title": "Hirschsprung-associated enterocolitis (HAEC): risk factors, prevention and treatment",
        "authors": ["Pastor AC", "Moses DL", "Teitelbaum DH"],
        "journal": "Seminars in Pediatric Surgery",
        "year": "2022",
        "abstract": "Review of HAEC in 892 patients over 15 years. HAEC incidence: 26% pre-op, 18% post-op. Risk factors: long-segment disease (OR 3.2), Down syndrome (OR 2.8), delayed diagnosis (OR 2.1), inadequate pull-through cuff length (OR 4.7). Preventive rectal irrigations (30 mL/kg normal saline, twice daily) reduced post-op HAEC by 47%. Treatment protocol: IV metronidazole + rectal irrigations q6–8h. Severe HAEC required diverting ostomy in 8%. Conclusion: HAEC remains the most serious complication; prevention with rectal irrigations and prompt IV antibiotic treatment are essential.",
        "doi": "10.1053/j.sempedsurg.2022.151234",
        "citations": 167,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36101234/",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "35992345",
        "title": "Neonatal versus delayed repair of Hirschsprung disease: impact on outcomes",
        "authors": ["Menezes M", "Das L", "Puri P"],
        "journal": "Pediatric Surgery International",
        "year": "2022",
        "abstract": "Comparison of outcomes in neonatal (< 28 days, n=142) vs delayed primary pull-through (>1 month, n=398) for HD. Neonatal group: higher anastomotic stricture rate (14% vs 6%, p=0.002), longer operative time, but no difference in continence at 5 years or HAEC rate. Staged approach (colostomy + delayed pull-through) in 12% of neonates. Conclusion: Delayed pull-through (after 1 month) may be preferable in stable neonates to reduce anastomotic complications, while neonatal primary repair is safe in experienced centers.",
        "doi": "10.1007/s00383-022-05234-6",
        "citations": 78,
        "source": "CrossRef",
        "url": "https://doi.org/10.1007/s00383-022-05234-6",
        "publication_types": ["Cohort Study"],
    },
]

# ── Hernia inguinal pediátrica ────────────────────────────────────────────── #
INGUINAL_HERNIA = [
    {
        "pmid": "37223456",
        "title": "Laparoscopic versus open inguinal hernia repair in children: RCT and meta-analysis",
        "authors": ["Shalaby R", "Ismail M", "Gouda H"],
        "journal": "Surgical Endoscopy",
        "year": "2023",
        "abstract": "RCT and meta-analysis (21 RCTs, n=3,412 children ages 0–14 years). Laparoscopic (percutaneous internal ring suturing, PIRS) vs open herniotomy. Primary endpoints: recurrence at 2 years, contralateral metachronous hernia, complications. Recurrence: laparoscopic 1.3% vs open 1.1% (p=0.78). Contralateral hernia at 2 years: laparoscopic 0.9% (PIRS detected & repaired) vs open 3.4% (p=0.001). Operative time similar. Laparoscopic: better cosmesis, bilateral exploration advantage. Hydrocele formation: laparoscopic 2.1% vs open 4.8%. Conclusion: Laparoscopic repair (PIRS) offers equivalent recurrence with the added benefit of contralateral exploration and repair in a single operation.",
        "doi": "10.1007/s00464-023-10034-5",
        "citations": 145,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37223456/",
        "publication_types": ["Meta-Analysis", "Randomized Controlled Trial"],
    },
    {
        "pmid": "36889234",
        "title": "Timing of inguinal hernia repair in premature infants: before versus after NICU discharge",
        "authors": ["Misra D", "Banerjee G", "Bhatnagar V"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2023",
        "abstract": "Retrospective study of 678 premature infants (gestational age <37 weeks) with inguinal hernia. Early repair before NICU discharge (n=312) vs repair after discharge (n=366). Pre-discharge repair: lower incarceration risk (0.6% vs 8.4%, p<0.001), higher anesthetic risk (post-extubation apnea 6.2% vs 1.1%). Postmenstrual age <44 weeks: highest apnea risk. Recommendation: repair before NICU discharge to prevent incarceration in stable infants >44 weeks PMA or with cardiorespiratory stability; caffeine prophylaxis for apnea. Conclusion: Timing requires individualized decision balancing incarceration vs anesthetic risk.",
        "doi": "10.1016/j.jpedsurg.2023.01.012",
        "citations": 112,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36889234/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Atresia esofágica ─────────────────────────────────────────────────────── #
ESOPHAGEAL_ATRESIA = [
    {
        "pmid": "37112345",
        "title": "Thoracoscopic versus open repair of esophageal atresia: international multicenter outcomes",
        "authors": ["Lugo B", "Malhotra A", "Lau ST"],
        "journal": "Annals of Surgery",
        "year": "2023",
        "abstract": "International multicenter cohort (IPSO registry, 18 centers, n=1,248 neonates) comparing thoracoscopic (TA, n=624) vs open thoracotomy (OT, n=624) repair of esophageal atresia (EA) with TEF. TA: lower musculoskeletal morbidity (scoliosis at 5 years: 4% vs 14%, p<0.001), similar anastomotic leak rate (12% vs 13%), similar stricture rate (28% vs 30%), longer operative time (105 vs 78 min). Learning curve: centers performing >30 TA/year showed comparable outcomes to open. Conclusion: TA is the preferred approach in experienced centers for reduction of long-term musculoskeletal complications; anastomotic outcomes are equivalent.",
        "doi": "10.1097/SLA.0000000000005456",
        "citations": 234,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37112345/",
        "publication_types": ["Cohort Study"],
    },
    {
        "pmid": "36998123",
        "title": "Long-gap esophageal atresia management: Foker versus Kimura versus primary repair outcomes",
        "authors": ["Foker JE", "Kendall TC", "Catton K"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2022",
        "abstract": "Multicenter retrospective comparison of strategies for long-gap EA (≥3 vertebral bodies gap). Foker technique (n=78): primary esophageal preservation, traction sutures for esophageal growth — anastomosis achieved in 91%, esophageal replacement avoided in 87%. Kimura technique (n=34): 78% primary esophageal anastomosis. Gastric pull-up (n=42): no anastomotic strictures but higher reflux (72%) and swallowing dysfunction. Quality of life at 5 years best with preserved esophagus. Conclusion: Foker technique allows esophageal preservation in most long-gap EA, but requires specialized surgical expertise; esophageal replacement reserved for failed primary repair strategies.",
        "doi": "10.1016/j.jpedsurg.2022.11.009",
        "citations": 167,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36998123/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Gastrosquisis / Onfalocele ────────────────────────────────────────────── #
ABDOMINAL_WALL = [
    {
        "pmid": "37334567",
        "title": "Primary versus staged closure of gastroschisis: systematic review and meta-analysis",
        "authors": ["Bradnock TJ", "Walker GM", "Fisher R"],
        "journal": "Archives of Disease in Childhood",
        "year": "2023",
        "abstract": "Systematic review of 29 studies (n=4,823 neonates) comparing primary fascial closure (PFC) vs staged silo reduction (SSR) for gastroschisis. PFC (when abdominal domain adequate): shorter time to full feeds (MD −5.8 days, 95% CI −8.2 to −3.4), shorter mechanical ventilation (MD −2.1 days), shorter hospital stay (MD −9.2 days), no difference in mortality or short bowel syndrome. SSR: safer when bowel compromise, solid viscera herniation, or poor abdominal compliance. 'Sutureless' or spring-loaded silo: comparable outcomes to formal SSR. Conclusion: PFC is preferred when feasible; SSR reserved for complex gastroschisis.",
        "doi": "10.1136/archdischild-2022-324789",
        "citations": 198,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/37334567/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
]

# ── Criptorquidia ─────────────────────────────────────────────────────────── #
CRYPTORCHIDISM = [
    {
        "pmid": "36556892",
        "title": "Timing of orchiopexy for cryptorchidism: effect on fertility and testicular cancer risk",
        "authors": ["Thorup J", "McLachlan R", "Cortes D"],
        "journal": "Journal of Urology",
        "year": "2023",
        "abstract": "Long-term cohort study (n=2,891 males, 30-year follow-up) evaluating orchiopexy timing in cryptorchidism. Orchiopexy at 6–12 months: paternity rate 89% bilateral, 92% unilateral. Orchiopexy at 12–24 months: bilateral 74%, unilateral 90%. Orchiopexy >2 years: bilateral 36%, unilateral 82%. Testicular cancer risk reduced with orchiopexy before age 10 (OR 0.42, 95% CI 0.28–0.63). Current guidelines recommend orchiopexy at 6–12 months of age. Conclusion: Early orchiopexy (6–12 months) maximizes fertility outcomes and reduces malignancy risk; delays beyond 18 months significantly impair spermatogenesis.",
        "doi": "10.1097/JU.0000000000003123",
        "citations": 189,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36556892/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Vólvulo de intestino medio / Malrotación ──────────────────────────────── #
MALROTATION = [
    {
        "pmid": "36778923",
        "title": "Ladd procedure for intestinal malrotation in neonates and children: laparoscopic versus open",
        "authors": ["Ledbetter DJ", "Juern A", "Arca MJ"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2023",
        "abstract": "Multicenter retrospective review of Ladd procedure in 892 patients (neonates 34%, infants 41%, children 25%). Laparoscopic (n=356) vs open (n=536). Laparoscopic: reduced hospital stay (3.2 vs 5.1 days, p<0.001), lower SSI rate (0.8% vs 4.2%, p<0.001). Conversion rate 14% (predominantly neonates with volvulus). Open preferred for midgut volvulus with bowel ischemia (28% of cases). Short bowel syndrome in 4.3% of volvulus cases. Conclusion: Laparoscopic Ladd procedure is safe and effective in stable patients; open approach mandatory in volvulus with ischemia. Appendectomy is performed routinely.",
        "doi": "10.1016/j.jpedsurg.2023.02.013",
        "citations": 143,
        "source": "Semantic Scholar",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36778923/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Estenosis de la unión ureteropélvica ─────────────────────────────────── #
UPJ_OBSTRUCTION = [
    {
        "pmid": "36667812",
        "title": "Robotic-assisted versus laparoscopic pyeloplasty in children: comparative outcomes",
        "authors": ["Lee RS", "Retik AB", "Borer JG"],
        "journal": "Journal of Urology",
        "year": "2023",
        "abstract": "Systematic review of 18 studies (n=1,245 children) comparing robotic-assisted (RAP) vs laparoscopic pyeloplasty (LP) for ureteropelvic junction obstruction. RAP: shorter learning curve, superior anastomotic accuracy, longer operative time (+22 min). Success rate: RAP 96.2% vs LP 94.8% (p=0.31). Complication rate similar (4.3% vs 4.8%). Hospital stay: RAP 1.6 vs LP 1.8 days. Cost: RAP 32% higher. Conclusion: Both approaches are equally effective; RAP offers technical advantages with shorter learning curve but higher cost; LP remains cost-effective standard in experienced hands.",
        "doi": "10.1097/JU.0000000000003256",
        "citations": 167,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36667812/",
        "publication_types": ["Meta-Analysis", "Systematic Review"],
    },
]

# ── Colecistitis / Colelitiasis pediátrica ────────────────────────────────── #
CHOLELITHIASIS = [
    {
        "pmid": "36889345",
        "title": "Pediatric cholelithiasis: risk factors, management, and outcomes of laparoscopic cholecystectomy",
        "authors": ["Svensson J", "Makin E", "Davenport M"],
        "journal": "Journal of Pediatric Surgery",
        "year": "2023",
        "abstract": "Multicenter cohort of 3,456 children (mean age 11.3 years) undergoing laparoscopic cholecystectomy for cholelithiasis. Risk factors: hemolytic disease (38%), obesity (32%), total parenteral nutrition (12%), idiopathic (18%). Laparoscopic success rate 97.8%; conversion 2.2%. Bile duct injury rate 0.06%. Same-day discharge achieved in 71%. Choledocholithiasis in 6.3% (managed by ERCP pre-op or intraoperative cholangiogram). Complication rate 3.1%. Conclusion: Laparoscopic cholecystectomy is safe and effective in children with similar outcomes to adults; same-day surgery is feasible in selected patients.",
        "doi": "10.1016/j.jpedsurg.2023.01.023",
        "citations": 112,
        "source": "PubMed",
        "url": "https://pubmed.ncbi.nlm.nih.gov/36889345/",
        "publication_types": ["Cohort Study"],
    },
]

# ── Registry mapping ─────────────────────────────────────────────────────── #
TOPIC_MAP = {
    "appendicitis": APPENDICITIS,
    "apendicitis": APPENDICITIS,
    "apendic": APPENDICITIS,
    "intussusception": INTUSSUSCEPTION,
    "intususception": INTUSSUSCEPTION,
    "invaginac": INTUSSUSCEPTION,
    "invaginación": INTUSSUSCEPTION,
    "pyloric": PYLORIC_STENOSIS,
    "piloro": PYLORIC_STENOSIS,
    "píloro": PYLORIC_STENOSIS,
    "estenosis hipertrófica": PYLORIC_STENOSIS,
    "hirschsprung": HIRSCHSPRUNG,
    "hirschsp": HIRSCHSPRUNG,
    "inguinal": INGUINAL_HERNIA,
    "hernia": INGUINAL_HERNIA,
    "esofágica": ESOPHAGEAL_ATRESIA,
    "esofagic": ESOPHAGEAL_ATRESIA,
    "esophag": ESOPHAGEAL_ATRESIA,
    "atresia": ESOPHAGEAL_ATRESIA,
    "gastrosquisis": ABDOMINAL_WALL,
    "gastroschis": ABDOMINAL_WALL,
    "onfalocele": ABDOMINAL_WALL,
    "omphalocele": ABDOMINAL_WALL,
    "criptorquidia": CRYPTORCHIDISM,
    "cryptorchid": CRYPTORCHIDISM,
    "orquiopexia": CRYPTORCHIDISM,
    "orchiopexy": CRYPTORCHIDISM,
    "malrotac": MALROTATION,
    "malrotation": MALROTATION,
    "ladd": MALROTATION,
    "vólvulo": MALROTATION,
    "volvulo": MALROTATION,
    "ureteropélvica": UPJ_OBSTRUCTION,
    "ureteropelvic": UPJ_OBSTRUCTION,
    "pieloplastia": UPJ_OBSTRUCTION,
    "pyeloplasty": UPJ_OBSTRUCTION,
    "colecistitis": CHOLELITHIASIS,
    "colelitiasis": CHOLELITHIASIS,
    "cholecystitis": CHOLELITHIASIS,
    "cholelithiasis": CHOLELITHIASIS,
    "vesícula": CHOLELITHIASIS,
}

# Generic pediatric surgery papers used when topic doesn't match a specific set
GENERIC_PEDS_SURGERY = (
    APPENDICITIS[:2]
    + INTUSSUSCEPTION[:1]
    + PYLORIC_STENOSIS[:1]
    + HIRSCHSPRUNG[:1]
    + INGUINAL_HERNIA[:1]
)


def get_demo_papers(topic: str) -> list[dict]:
    """Return demo papers best matching the topic in pediatric surgery."""
    topic_lower = topic.lower()
    for keyword, papers in TOPIC_MAP.items():
        if keyword in topic_lower:
            return papers
    return GENERIC_PEDS_SURGERY
