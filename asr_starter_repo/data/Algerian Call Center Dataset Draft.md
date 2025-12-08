# Algerian Call Center Dataset Draft

This document outlines the initial content generation for a comprehensive Algerian Call Center Dataset, focusing on customer service interactions in Algerian Arabic (Darija). The dataset is structured to cover common scenarios in key sectors like telecommunications, banking, and utilities, incorporating the linguistic and cultural nuances of the Algerian market.

## 1. Dataset Structure

The dataset will be generated in a tabular format, with the following columns:

| Column Name | Description | Example Content |
| :--- | :--- | :--- |
| **ID** | Unique identifier for the interaction. | CC-TEL-001 |
| **Sector** | The industry sector of the call. | Telecommunications |
| **Topic** | The specific subject of the customer's query/complaint. | Internet Outage |
| **Customer_Query_AR** | The customer's statement in Algerian Arabic (Darija). | راني مقطوع من الإنترنت من البارح، ما حبش يمشي خلاص. |
| **Customer_Query_FR** | The customer's statement in French (common in Algeria). | Mon internet est coupé depuis hier, il ne veut plus marcher du tout. |
| **Customer_Query_EN** | The customer's statement in English (for international use). | My internet has been cut off since yesterday, it won't work at all. |
| **Agent_Response_AR** | The call center agent's appropriate response in Darija. | آسف على الإزعاج، ممكن تعطيني رقم الخط تاعك باش نشوف المشكل؟ |
| **Agent_Response_FR** | The agent's response in French. | Je suis désolé pour le désagrément, pouvez-vous me donner votre numéro de ligne pour que je puisse vérifier le problème ? |
| **Agent_Action** | The required action the agent must take. | Check line status, create trouble ticket. |
| **Sentiment** | The customer's initial sentiment (e.g., Angry, Frustrated, Neutral). | Frustrated |

## 2. Initial Content Generation (Telecommunications Sector)

This section focuses on common issues with **Algérie Télécom** and mobile operators, which are frequently cited in online discussions.

| ID | Sector | Topic | Customer_Query_AR | Customer_Query_FR | Customer_Query_EN | Agent_Response_AR | Agent_Response_FR | Agent_Action | Sentiment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CC-TEL-001 | Telecommunications | Internet Outage | راني مقطوع من الإنترنت من البارح، ما حبش يمشي خلاص. | Mon internet est coupé depuis hier, il ne veut plus marcher du tout. | My internet has been cut off since yesterday, it won't work at all. | آسف على الإزعاج، ممكن تعطيني رقم الخط تاعك باش نشوف المشكل؟ | Je suis désolé pour le désagrément, pouvez-vous me donner votre numéro de ligne pour que je puisse vérifier le problème ? | Check line status, create trouble ticket. | Frustrated |
| CC-TEL-002 | Telecommunications | Slow Speed | الكونيكسيون ثقيلة بزاف، ما نقدر ندير والو. | La connexion est très lente, je ne peux rien faire. | The connection is very slow, I can't do anything. | فهمتك، السرعة ضعيفة. هل جربت تعاود تشعل المودم؟ | Je comprends, la vitesse est faible. Avez-vous essayé de redémarrer votre modem ? | Guide customer through modem restart, check subscription plan. | Annoyed |
| CC-TEL-003 | Telecommunications | Billing Inquiry | جاتني فاتورة غالية بزاف هذا الشهر، علاش؟ | Ma facture est très chère ce mois-ci, pourquoi ? | My bill is very expensive this month, why? | ممكن تعطيني رقم الزبون تاعك باش نراجعو تفاصيل الفاتورة؟ | Pouvez-vous me donner votre numéro de client pour que nous puissions examiner les détails de la facture ? | Access billing history, explain charges. | Confused |
| CC-TEL-004 | Telecommunications | Service Activation | حبيت نأكتيفي عرض جديد تاع 4G، كيفاش ندير؟ | Je veux activer une nouvelle offre 4G, comment faire ? | I want to activate a new 4G offer, how do I do it? | تفضل، ممكن تبعث *700# وتتبع الخطوات. | Bien sûr, vous pouvez composer le *700# et suivre les étapes. | Provide USSD code or activation steps. | Neutral |
| CC-TEL-005 | Telecommunications | Technical Support | المودم تاعي راه يشعل ويطفى وحدو، واش المشكل؟ | Mon modem s'allume et s'éteint tout seul, quel est le problème ? | My modem turns on and off by itself, what's the problem? | هذا ممكن يكون مشكل تقني، ممكن تخليلي رقمك ونتصل بك تقني؟ | Cela pourrait être un problème technique, pouvez-vous me laisser votre numéro et un technicien vous rappellera ? | Schedule a technician callback. | Worried |

## 3. Initial Content Generation (Banking Sector)

This section focuses on common issues with **electronic payments, card services, and account inquiries** in Algerian banks (e.g., BNA, CPA).

| ID | Sector | Topic | Customer_Query_AR | Customer_Query_FR | Customer_Query_EN | Agent_Response_AR | Agent_Response_FR | Agent_Action | Sentiment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CC-BNK-001 | Banking | Card Blocked | لاكارط تاعي بلوكات، ما قدرتش نجبد دراهم. | Ma carte est bloquée, je n'ai pas pu retirer d'argent. | My card is blocked, I couldn't withdraw money. | آسف، ممكن تعطيني رقم البطاقة تاعك ونتأكد من الحالة؟ | Je suis désolé, pouvez-vous me donner votre numéro de carte pour que je vérifie le statut ? | Verify card status, unblock if possible, or advise on replacement. | Urgent |
| CC-BNK-002 | Banking | Transaction Dispute | صراتلي عملية شراء ما درتهاش، لازم نلغيها. | J'ai eu une transaction que je n'ai pas faite, je dois l'annuler. | I had a transaction I didn't make, I need to cancel it. | من فضلك، سجل محضر شكوى في أقرب وكالة، وراح نفتحو تحقيق. | S'il vous plaît, déposez une plainte à l'agence la plus proche, et nous ouvrirons une enquête. | Advise on dispute process, open investigation ticket. | Concerned |
| CC-BNK-003 | Banking | Account Balance | حبيت نعرف شحال بقالي دراهم في الكونط. | Je veux savoir combien il me reste d'argent sur mon compte. | I want to know how much money I have left in my account. | لأسباب أمنية، ما نقدرش نعطيك الرصيد مباشرة. ممكن تستعمل تطبيق البنك أو الصراف الآلي. | Pour des raisons de sécurité, je ne peux pas vous donner le solde directement. Vous pouvez utiliser l'application bancaire ou le GAB. | Advise on secure methods for balance check. | Neutral |

## 4. Initial Content Generation (Utilities Sector)

This section focuses on common issues with **water and electricity services** (e.g., Sonelgaz, ADE).

| ID | Sector | Topic | Customer_Query_AR | Customer_Query_FR | Customer_Query_EN | Agent_Response_AR | Agent_Response_FR | Agent_Action | Sentiment |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| CC-UTL-001 | Utilities | Water Cut | الماء مقطوع في الحومة تاعنا من الصباح. | L'eau est coupée dans notre quartier depuis ce matin. | The water has been cut off in our neighborhood since this morning. | آسف، ممكن تعطيني العنوان بالضبط باش نبعثو فريق الصيانة؟ | Je suis désolé, pouvez-vous me donner l'adresse exacte pour que nous envoyions l'équipe de maintenance ? | Log outage report, dispatch maintenance team. | Impatient |
| CC-UTL-002 | Utilities | Electricity Meter | العداد تاع الضو راه يدور بالخف، كاين مشكل. | Le compteur d'électricité tourne très vite, il y a un problème. | The electricity meter is spinning very fast, there's a problem. | هذا ممكن يكون مشكل في العداد، راح نبعثو تقني يفحصو في أقرب وقت. | Cela pourrait être un problème avec le compteur, nous allons envoyer un technicien pour le vérifier dès que possible. | Schedule meter inspection. | Suspicious |
| CC-UTL-003 | Utilities | New Subscription | حبيت ندير اشتراك جديد تاع الغاز. | Je veux faire un nouvel abonnement au gaz. | I want to get a new gas subscription. | تفضل، لازم تجيب ملف فيه نسخة من بطاقة التعريف وعقد الإيجار للوكالة. | Bien sûr, vous devez apporter un dossier contenant une copie de votre carte d'identité et le contrat de location à l'agence. | List required documents and direct to nearest agency. | Neutral |

## 5. Linguistic and Cultural Notes

The responses are formulated using a mix of **Standard Arabic (Fusha)** and **Algerian Darija**, which is typical for formal customer service in Algeria. French is also included as it is a common language for communication in the country.

*   **Darija Terms Used:**
    *   **مقـطوع** (Maqṭūʿ): Cut off (for service).
    *   **حومة** (Ḥūma): Neighborhood.
    *   **الكونيكسيون** (El-Connexion): Internet connection (French loanword).
    *   **دراهم** (Drāhem): Money.
    *   **لاكارط** (La Carte): Card (French loanword).
    *   **الضو** (Eḍ-ḍaw): Electricity/Light.
    *   **الغاز** (El-Gāz): Gas.
    *   **واش المشكل** (Wāsh el-mushkil): What is the problem?

This initial draft provides 11 high-quality, multi-lingual examples across three key sectors. The next phase will involve refining and expanding this content.
