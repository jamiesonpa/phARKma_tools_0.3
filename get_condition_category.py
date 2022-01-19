import phARKma_utils
import pandas as pd

def get_condition_category(trial_row):
    blood=("blood",["heme","anemia","erythro","leuco","hemo","thrombo","thromb","clotting","coagula","basophil","marrow","gout","myelofibrosis","venous","angio","phleb","plasma","platelet","red blood cell","macroglob","macrophage","neutrophil","blood"])
    oncological=("oncological",["carcinoma","leukemia","cancer","cancer","cancer","cancer","cancer","cancer","cancer","tumor","cancer","neoplasm","sarcoma","myeloma","angioma","thelioma","chemotherapy","aplastic","metast","cytomegaly","leukemia"])
    cardiovascular=("cardiovascular",["cardio","aortic","aorta","heart","deep vein","thrombosis","coronary","artery","arteri","statin","beta blocker","angioplasty","valve","carditi","rheumatic","myopathy","hypertens","hypotens","rhythmia","stenos"])
    congential=("congential",["genetic","congenital","hereditary","trisomy","deletion","chromosom","monosomy","ploidy","translocation","mutation"])
    ear=("ear",["tinnitus","otitis","eustac","tympani","vestibular","vestibu","perichondritis","auriculo","deaf","meniere"])
    eye=("eye",["myopia","myopic","macula","cornea","orbit","iris","pupil","glaucoma","cataract","refractive","retino","strabis","amblyop","optic","eye","diplopia"])
    infection=("infection",["infection","pathogen","patho","viral","fungal","bacteri","parasit","myco","biotic","antibiotic","septic","sepsis","toxin","fever","hyperpyrexia","virus","bacter","yeast"])
    rheumatological=("rheumatological",["autoimmune","inflammation","inflam","arthrit","lupus","allerg","immun","histo","lymph","transplant","xenogra"])
    trauma=("trauma",["injury","trauma","cut","laceration","incision","accident","wound","sprain","fracture","contusion","hematoma","range of motion","strain","tear"])
    mental_health=("mental_health",["psycho","mania","bipolar","dementia","behavior","wellness","cogn","depress","manic","mood","schizo","hallucin","delusion"])
    metabolic_and_endocrine=("metabolic_and_endocrine",["nutrition","adrenal", "adreno","pancrea","pituitar","endocrine","hormone","estrogen","testosterone","thyroid","corticosteroid","steroid","diabetes","deficien","vitamin"])
    musculoskeletal=("musculoskeletal",["tendon","ligament","muscle","musculo","neuritis","disc","synovi","syno","fascia"])
    neurological=("neurological",["seizure","epilepsy","neuro","sclerosis","amnesia","cephaly","cepha","astrocy","axon","myelin","cerebel","cerebr","chiasm","cauda eq","cortex","cranio","cranie","dura","nystagmus","arachnoid","neura"])
    oral_and_gastrointestinal=("oral_and_gastrointestinal",["gastric","gastrointestical","phagia","esophag","gastro","anus","bile","biliary","bowel","colectomy","colon","colitis","diverti","entera","enteric","entero","hemorr","hepatic","liver","hepato","ileo","ileum","jejun","intesti","laparo","manomet","nasogas","scinti","sigmoid colon","sphincter"])
    renal_and_urogenital=("renal_and_urogenital",["renal","renal","renal","renal","renal","kidney","penis","vagina","uterus","cervix","testicu","testes","testicle","ovary","ovari"])
    reproductive=("reproductive",["fertility", "fertil","genito","pregnancy","eclampsia","endomet","amnio","contraction","delivery","breech","gestatio","meconium","tear","caesarean"])
    respiratory=("respiratory",["lung","mesothelioma","broncho","respiratory","athsma","pleur","pneumo","apnea","sarcoidosis","apnoea","respir","chest","alveol","cystic fibrosis","emphy","expirato","laryn","pharyn"])
    skin=("skin",["acne","derm","skin","mole","pigment","follic","epiderm","papul","kerato","keratos","keratin","licheno","pityr","verruc","wart"])
    stroke=("stroke",["stroke","aphasia","agnosia","aneurysm","arteriovenous malformation","apraxia","dysarthria","paresis","plagia","lacunar","ischemic","grand mal","intracerebral hemo"])
    idiopathic_other=("idiopathic",["idiopathic", "surgery","surgical","surger","device","prosthe"])

    categories = [blood, oncological, cardiovascular, congential, ear, eye, infection, rheumatological, trauma, mental_health, metabolic_and_endocrine, musculoskeletal, neurological, oral_and_gastrointestinal, renal_and_urogenital,respiratory, reproductive, skin, stroke, idiopathic_other]

    scores = {}
    for cat in categories:
        scores[cat[0]] = 0

    total_scores = {}
    for cat in categories:
        total_scores[cat[0]] = 0

    row_scores = {}
    for cat in categories:
        row_scores[cat[0]] = 0


    average_proportion = ["0.120894955","0.115857666","0.076219833","0.014147466","0.002708593","0.018878173","0.07240221","0.092899941","0.059583047","0.069212415","0.045252964","0.043655401","0.052166408","0.07203831","0.025136463","0.053662666","0.025193114","0.024068755","0.014693984","0.001327637"]
    average_scores = {}
    counter = 0
    for cat in categories:
        average_scores[cat[0]] = average_proportion[counter]
        counter +=1
    
    for key in row_scores.keys():
        row_scores[key] = 0

    if trial_row["CONDITION"].find("not found") == -1:
        trial_string = trial_row["CONDITION"].lower()

        trial_string = trial_string.lower()
        for cat in categories:
            for kw in cat[1]:
                if trial_string.find(kw) != -1:
                    row_scores[cat[0]] = row_scores[cat[0]] + trial_string.count(kw)
        
        total_scores = 0
        for key in row_scores.keys():
            total_scores = total_scores + row_scores[key]
        
        if total_scores > 0:
            normalized_scores = {}
            for key in row_scores.keys():
                normalized_scores[key] = row_scores[key]/total_scores
            
            multiple_scores = {}
            for key in row_scores.keys():
                multiple_scores[key] = 0

            for key in normalized_scores.keys():
                multiple_scores[key] = float(normalized_scores[key])/float(average_scores[key])
            
            highest = 0
            primary_probable_cat = ""
            for key in multiple_scores.keys():
                if multiple_scores[key] > highest:
                    highest = multiple_scores[key]
                    primary_probable_cat = key
            
            highest2 = 0
            secondary_probable_cat = ""
            keys = []
            for key in multiple_scores.keys():
                if key != primary_probable_cat:
                    if key != "":
                        if key != " ":
                            keys.append(key)
            for key in keys:
                if float(multiple_scores[key]) > float(highest2):
                    highest2 = multiple_scores[key]
                    secondary_probable_cat = key

            # print("Found that " + trial_row["CONDITION"] + " is most likely a " + primary_probable_cat + " or " + secondary_probable_cat + " type disease")

            probable_disease_categories = (primary_probable_cat, secondary_probable_cat)
            return probable_disease_categories