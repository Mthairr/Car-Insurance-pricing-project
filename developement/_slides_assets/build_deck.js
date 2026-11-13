const pptxgen = require("pptxgenjs");
const path = require("path");

const ASSETS = __dirname;
const OUT = path.join(ASSETS, "..", "..", "Soutenance_Association_Variables.pptx");

const THEME = {
  name: "AssociationVariables",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1E2761",
    lt1: "FFFFFF",
    dk2: "10163B",
    lt2: "CADCFC",
    accent1: "F2A93B",
    accent2: "6B7A99",
    accent3: "3B4F8A",
    accent4: "CADCFC",
    accent5: "D97B29",
    accent6: "9FB3D9",
    hlink: "F2A93B",
    folHlink: "D97B29",
  },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.company = "Pricing Assurance Auto";

const C = pres.SchemeColor;
const NAVY = THEME.colors.dk1;
const DARK = THEME.colors.dk2;
const ICE = THEME.colors.lt2;
const AMBER = THEME.colors.accent1;
const SLATE = THEME.colors.accent2;
const BLUE2 = THEME.colors.accent3;
const AMBER2 = THEME.colors.accent5;
const CARD_BG = "EEF3FC"; // very light ice tint for cards

const W = 13.33, H = 7.5;

// ---------- Slide masters (layouts) ----------
pres.defineSlideMaster({
  title: "TITLE_DARK",
  background: { color: DARK },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.9, y: 2.75, w: 11.5, h: 1.4, fontFace: THEME.headFontFace, fontSize: 40, bold: true, color: "FFFFFF", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.9, y: 4.15, w: 11.0, h: 0.9, fontFace: THEME.bodyFontFace, fontSize: 18, color: ICE, align: "left" }, text: "" } },
    { text: { options: { x: 0.9, y: 6.9, w: 8, h: 0.4, fontFace: THEME.bodyFontFace, fontSize: 11, color: SLATE }, text: "Pricing Assurance Auto — Association entre variables" } },
  ],
});

pres.defineSlideMaster({
  title: "DIVIDER_DARK",
  background: { color: DARK },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.9, y: 3.15, w: 11.5, h: 1.2, fontFace: THEME.headFontFace, fontSize: 32, bold: true, color: "FFFFFF", align: "left" }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.9, y: 4.35, w: 10.5, h: 0.6, fontFace: THEME.bodyFontFace, fontSize: 15, color: ICE, align: "left" }, text: "" } },
    { text: { options: { x: 12.3, y: 7.05, w: 0.6, h: 0.3, fontFace: THEME.bodyFontFace, fontSize: 10, color: SLATE, align: "right" }, text: "" } },
  ],
  slideNumber: { x: 12.5, y: 7.1, color: SLATE, fontSize: 10, fontFace: THEME.bodyFontFace },
});

pres.defineSlideMaster({
  title: "CONTENT_LIGHT",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.45, w: 11.9, h: 0.85, fontFace: THEME.headFontFace, fontSize: 28, bold: true, color: NAVY, align: "left" }, text: "" } },
    { text: { options: { x: 0.7, y: 1.28, w: 11.9, h: 0.02, fill: { color: "FFFFFF" }, line: { color: "FFFFFF" } }, text: "" } },
  ],
  slideNumber: { x: 12.7, y: 7.1, color: SLATE, fontSize: 10, fontFace: THEME.bodyFontFace },
});

pres.defineSlideMaster({
  title: "CONTENT_TABLE",
  background: { color: "FFFFFF" },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.45, w: 11.9, h: 0.85, fontFace: THEME.headFontFace, fontSize: 28, bold: true, color: NAVY, align: "left" }, text: "" } },
    { placeholder: { options: { name: "table", type: "body", x: 0.7, y: 1.5, w: 11.9, h: 5.4 }, text: "" } },
  ],
  slideNumber: { x: 12.7, y: 7.1, color: SLATE, fontSize: 10, fontFace: THEME.bodyFontFace },
});

// ---------- Helpers ----------
function addFooterNote(slide, txt) {
  slide.addText(txt, { x: 0.7, y: 7.08, w: 11.5, h: 0.3, fontFace: THEME.bodyFontFace, fontSize: 10, color: SLATE, italic: true, isTextBox: true, margin: 0 });
}

function statCard(slide, x, y, w, h, value, label, color) {
  slide.addShape("roundRect", { x, y, w, h, rectRadius: 0.1, fill: { color: CARD_BG }, line: { type: "none" }, shadow: { type: "outer", color: "1E2761", opacity: 0.12, blur: 6, offset: 2, angle: 90 } });
  slide.addText(value, { x, y: y + 0.18, w, h: h - 0.75, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 30, bold: true, color: color || NAVY, isTextBox: true, margin: 0 });
  slide.addText(label, { x: x + 0.15, y: y + h - 0.62, w: w - 0.3, h: 0.55, align: "center", valign: "top", fontFace: THEME.bodyFontFace, fontSize: 11, color: SLATE, isTextBox: true, margin: 0 });
}

function numberedCircle(slide, x, y, d, num) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: NAVY }, line: { type: "none" } });
  slide.addText(String(num), { x, y, w: d, h: d, align: "center", valign: "middle", fontFace: THEME.headFontFace, fontSize: 22, bold: true, color: "FFFFFF", isTextBox: true, margin: 0 });
}

// =====================================================================
// SECTION 1 — Introduction
// =====================================================================
pres.addSection({ title: "Introduction" });

// Slide 1 — Title
let s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Introduction" });
s.addText("Association entre variables : choisir les bonnes variables", { placeholder: "title" });
s.addText("Pricing assurance auto — fréquence × sévérité des sinistres", { placeholder: "body" });
s.addShape("line", { x: 0.9, y: 2.5, w: 1.3, h: 0, line: { color: AMBER, width: 3 } });
s.addText("Soutenance de projet — Data Science", { x: 0.9, y: 5.1, w: 8, h: 0.4, fontFace: THEME.bodyFontFace, fontSize: 13, color: SLATE, isTextBox: true, margin: 0 });

// Slide 2 — Problématique
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Introduction" });
s.addText("La problématique de modélisation", { placeholder: "title" });
s.addText(
  "Objectif : estimer la prime pure = P(sinistre) × E[montant | sinistre]\nDeux modèles à construire, à partir d'un même socle de variables explicatives brutes (véhicule, conducteur, contrat).",
  { x: 0.7, y: 1.45, w: 11.9, h: 0.95, fontFace: THEME.bodyFontFace, fontSize: 15, color: NAVY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2 }
);
const probCards = [
  { v: "17", l: "variables explicatives candidates (fréquence)" },
  { v: "9+8", l: "variables numériques et catégorielles (sévérité)" },
  { v: "?", l: "Lesquelles garder, lesquelles éliminer, et pourquoi" },
];
const cw = 3.7, gap = 0.4, startX = 0.7;
probCards.forEach((c, i) => statCard(s, startX + i * (cw + gap), 2.7, cw, 1.9, c.v, c.l, i === 2 ? AMBER2 : NAVY));
s.addText(
  "Le fil conducteur de cette soutenance : justifier le choix des variables de chaque modèle à partir des résultats d'association statistique obtenus — entre variables explicatives, et avec les cibles.",
  { x: 0.7, y: 5.1, w: 11.9, h: 1.3, fontFace: THEME.bodyFontFace, fontSize: 15, italic: true, color: BLUE2, isTextBox: true, margin: 0, lineSpacingMultiple: 1.25 }
);

// Slide 3 — Démarche en 4 phases
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Introduction" });
s.addText("Démarche en 4 phases", { placeholder: "title" });
const phases = [
  { t: "Exploration descriptive", d: "Nettoyage, distributions, valeurs aberrantes" },
  { t: "Lien avec les cibles", d: "Corrélations / tests vs sinistre et montant" },
  { t: "Association entre variables", d: "8 métriques de redondance (ce focus)" },
  { t: "Modélisation & validation", d: "Choix de variables, entraînement, test" },
];
const pw = 2.75, pgap = 0.25, px0 = 0.75, py = 2.3, pd = 0.9;
phases.forEach((p, i) => {
  const x = px0 + i * (pw + pgap);
  numberedCircle(s, x + pw / 2 - pd / 2, py, pd, i + 1);
  if (i < phases.length - 1) {
    s.addShape("line", { x: x + pw - 0.05, y: py + pd / 2, w: pgap + 0.1, h: 0, line: { color: SLATE, width: 2, dashType: "dash" } });
  }
  s.addText(p.t, { x: x - 0.15, y: py + pd + 0.25, w: pw + 0.3, h: 0.7, align: "center", fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: i === 2 ? AMBER2 : NAVY, isTextBox: true, margin: 0 });
  s.addText(p.d, { x: x - 0.1, y: py + pd + 0.95, w: pw + 0.2, h: 1.0, align: "center", fontFace: THEME.bodyFontFace, fontSize: 12, color: SLATE, isTextBox: true, margin: 0 });
});
s.addText("Cette soutenance se concentre sur la phase 3 : l'association entre variables explicatives, et son impact direct sur le choix des variables des phases suivantes.", {
  x: 0.75, y: 5.9, w: 11.8, h: 0.8, fontFace: THEME.bodyFontFace, fontSize: 14, italic: true, color: BLUE2, isTextBox: true, margin: 0,
});

// Slide 4 — 8 métriques (table)
s = pres.addSlide({ masterName: "CONTENT_TABLE", sectionTitle: "Introduction" });
s.addText("8 métriques pour diagnostiquer les associations", { placeholder: "title" });
const headerRow = [
  { text: "Métrique", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } },
  { text: "Type de paire", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } },
  { text: "Ce qu'elle révèle", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } },
];
const rowsData = [
  ["Écart Pearson / Spearman", "Numérique × Numérique", "Non-linéarité de la relation"],
  ["VIF (facteur d'inflation)", "Numérique × Numérique", "Redondance multicolinéaire (régression)"],
  ["Indice de conditionnement", "Ensemble numérique", "Instabilité globale de la matrice"],
  ["V de Cramér (corrigé)", "Catégorielle × Catégorielle", "Association entre modalités"],
  ["Oméga² (corrigé)", "Catégorielle × Numérique", "Part de variance expliquée"],
  ["Information mutuelle", "Numérique × Numérique", "Dépendance non-linéaire générale"],
  ["Clustering hiérarchique", "Ensemble numérique", "Blocs de variables redondantes"],
  ["Permutation importance (bloc)", "Variable(s) × Modèle", "Preuve sur le modèle final"],
];
const tableRows = [headerRow, ...rowsData.map((r, i) => r.map((txt, j) => ({ text: txt, options: { color: NAVY, fontSize: 12, fill: { color: i % 2 === 0 ? "FFFFFF" : CARD_BG }, bold: j === 0 } })))];
s.addTable(tableRows, { x: 0.7, y: 1.55, w: 11.9, h: 5.2, colW: [3.6, 3.2, 5.1], fontFace: THEME.bodyFontFace, fontSize: 12, border: { type: "solid", color: "D9E2F3", pt: 0.75 }, autoPage: false, valign: "middle" });

// =====================================================================
// SECTION 2 — Constats d'association
// =====================================================================
pres.addSection({ title: "Constats d'association" });

// Slide 5 — Divider
s = pres.addSlide({ masterName: "DIVIDER_DARK", sectionTitle: "Constats d'association" });
s.addText("Ce que révèle l'analyse d'association", { placeholder: "title" });
s.addText("4 constats, obtenus sur les variables explicatives du jeu de données assurance auto", { placeholder: "body" });

// Slide 6 — Constat 1: liens faibles avec les cibles
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Constats d'association" });
s.addText("Constat 1 — Des liens individuels faibles avec les cibles", { placeholder: "title" });
statCard(s, 0.7, 1.6, 3.7, 2.3, "0,085", "Spearman max |ρ| — ancienneté du véhicule vs montant (log)", AMBER2);
statCard(s, 4.6, 1.6, 3.7, 2.3, "1 / 8", "variable catégorielle significative (Kruskal-Wallis) : type_contrat (p = 0,0000)", AMBER2);
statCard(s, 8.5, 1.6, 3.7, 2.3, "0,629", "ROC AUC test du modèle fréquence (naïf = 0,500)", NAVY);
s.addText(
  "Aucune variable, prise seule, n'explique fortement la survenance ou le coût d'un sinistre. Le signal est diffus : c'est la combinaison des variables, et leur structure de redondance, qui doit guider le choix — d'où l'importance de l'analyse d'association entre explicatives.",
  { x: 0.7, y: 4.25, w: 11.9, h: 1.6, fontFace: THEME.bodyFontFace, fontSize: 15, color: NAVY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.3 }
);

// Slide 7 — Constat 2: corrélations fortes entre explicatives (heatmap)
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Constats d'association" });
s.addText("Constat 2 — De fortes corrélations entre variables explicatives", { placeholder: "title" });
s.addImage({ path: path.join(ASSETS, "heatmap_spearman.png"), x: 0.7, y: 1.5, w: 6.7, h: 5.6 });
s.addText("Corrélations de Spearman (|ρ| > 0,5)", { x: 7.65, y: 1.55, w: 4.95, h: 0.4, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
const pairs = [
  "age_conducteur2 / anciennete_permis2 : 0,997",
  "anciennete_vehicule / debut_vente : 0,961",
  "debut_vente / fin_vente : 0,949",
  "age_conducteur1 / anciennete_permis1 : 0,925",
  "din_vehicule / prix_vehicule : 0,875",
  "poids_vehicule / prix_vehicule : 0,862",
  "cylindre_vehicule / prix_vehicule : 0,785",
];
s.addText(pairs.map((p) => ({ text: p, options: { bullet: { code: "2022", indent: 14 }, breakLine: true, paraSpaceAfter: 6 } })), { x: 7.65, y: 2.05, w: 4.95, h: 3.2, fontFace: THEME.bodyFontFace, fontSize: 12.5, color: NAVY, isTextBox: true, margin: 0 });
s.addText("Conséquence directe : VIF > 10 pour 6 variables, indice de conditionnement = 130,9. Une régression linéaire classique serait instable sur ce socle de variables.", {
  x: 7.65, y: 5.4, w: 4.95, h: 1.6, fontFace: THEME.bodyFontFace, fontSize: 12.5, italic: true, color: BLUE2, isTextBox: true, margin: 0, lineSpacingMultiple: 1.25,
});

// Slide 8 — Constat 3: 4 blocs redondants (dendrogram)
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Constats d'association" });
s.addText("Constat 3 — Les variables se regroupent en 4 blocs redondants", { placeholder: "title" });
s.addImage({ path: path.join(ASSETS, "dendrogramme.png"), x: 0.7, y: 1.5, w: 7.9, h: 4.35 });
const clusters = [
  { t: "Âge du véhicule", d: "anciennete_vehicule, debut_vente, fin_vente" },
  { t: "Puissance / gabarit", d: "din, cylindre, poids, vitesse, prix" },
  { t: "Ancienneté conducteur 1", d: "age_conducteur1, anciennete_permis1" },
  { t: "Ancienneté conducteur 2", d: "age_conducteur2, anciennete_permis2" },
];
clusters.forEach((cl, i) => {
  const x = 8.75 + (i % 1) * 0, y = 1.5 + i * 1.3;
  s.addShape("roundRect", { x: 8.75, y, w: 3.9, h: 1.15, rectRadius: 0.08, fill: { color: CARD_BG }, line: { type: "none" } });
  s.addText(cl.t, { x: 8.9, y: y + 0.08, w: 3.6, h: 0.4, fontFace: THEME.headFontFace, fontSize: 13, bold: true, color: NAVY, isTextBox: true, margin: 0 });
  s.addText(cl.d, { x: 8.9, y: y + 0.48, w: 3.6, h: 0.6, fontFace: THEME.bodyFontFace, fontSize: 10.5, color: SLATE, isTextBox: true, margin: 0 });
});
s.addText("Clustering hiérarchique (distance = 1 − |Spearman|, seuil 0,5) — hors blocs : bonus, durée contrat, ancienneté info restent isolées.", {
  x: 0.7, y: 6.0, w: 7.9, h: 0.7, fontFace: THEME.bodyFontFace, fontSize: 11, italic: true, color: SLATE, isTextBox: true, margin: 0,
});

// Slide 9 — Constat 4 / La preuve : individuel vs groupé
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Constats d'association" });
s.addText("La preuve — permutation individuelle vs. groupée", { placeholder: "title" });
s.addText("Modèle fréquence (Random Forest) — perte de ROC AUC quand on mélange la variable (ou le bloc corrélé)", {
  x: 0.7, y: 1.3, w: 11.9, h: 0.4, fontFace: THEME.bodyFontFace, fontSize: 13, color: SLATE, isTextBox: true, margin: 0,
});
const permChartData = [
  {
    name: "Permutation individuelle (moyenne du groupe)",
    labels: ["Âge du véhicule", "Puissance / gabarit", "type_contrat (témoin)"],
    values: [-0.02, 0.15, 2.39],
  },
  {
    name: "Permutation groupée (bloc complet)",
    labels: ["Âge du véhicule", "Puissance / gabarit", "type_contrat (témoin)"],
    values: [5.05, 3.29, 2.39],
  },
];
s.addChart("bar", permChartData, {
  x: 0.7, y: 1.85, w: 11.9, h: 4.3,
  barDir: "bar", barGrouping: "clustered", barGapWidthPct: 35,
  catAxisMultiLevelLabels: true,
  chartColors: [SLATE, AMBER],
  showTitle: false, showLegend: true, legendPos: "b", legendColor: NAVY, legendFontFace: "+mn-lt",
  showValue: true, dataLabelPosition: "outEnd", dataLabelColor: NAVY, dataLabelFontSize: 11, dataLabelFontFace: "+mn-lt",
  catAxisLabelColor: NAVY, catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 12,
  valAxisLabelColor: NAVY, valAxisLabelFontFace: "+mn-lt", valAxisTitle: "Perte d'AUC (points ×100)", showValAxisTitle: true,
  valGridLine: { color: "E6ECF8", size: 0.75 }, catGridLine: { style: "none" },
});
s.addText(
  "Prises isolément, les variables corrélées (âge du véhicule, puissance/gabarit) semblent inutiles — elles se compensent entre elles. Mélangées en bloc, leur importance réelle apparaît (jusqu'à 0,0505 d'AUC). type_contrat, non corrélée, sert de témoin : son effet ne change pas.",
  { x: 0.7, y: 6.3, w: 11.9, h: 0.9, fontFace: THEME.bodyFontFace, fontSize: 13, italic: true, color: BLUE2, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2 }
);

// =====================================================================
// SECTION 3 — Choix des variables & modélisation
// =====================================================================
pres.addSection({ title: "Choix des variables & modélisation" });

// Slide 10 — Choix final des variables
s = pres.addSlide({ masterName: "CONTENT_TABLE", sectionTitle: "Choix des variables & modélisation" });
s.addText("Le choix final des variables, justifié par l'association", { placeholder: "title" });
s.addText("Modèle fréquence — 15 variables retenues sur 17", { x: 0.7, y: 1.4, w: 5.8, h: 0.4, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
const freqRows = [
  [{ text: "Retrait", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } }, { text: "Justification", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } }],
  ["essence_vehicule", "Importance groupée ≈ 0,0001 (redondant avec modele_vehicule, V de Cramér 0,745)"],
  ["type_vehicule", "Importance groupée = 0,0000 (redondant avec modele_vehicule, V de Cramér 0,791)"],
].map((r, i) => (i === 0 ? r : r.map((t, j) => ({ text: t, options: { color: NAVY, fontSize: 12, fill: { color: i % 2 === 0 ? CARD_BG : "FFFFFF" }, bold: j === 0 } }))));
s.addTable(freqRows, { x: 0.7, y: 1.85, w: 5.8, h: 1.7, colW: [2.1, 3.7], fontFace: THEME.bodyFontFace, fontSize: 12, border: { type: "solid", color: "D9E2F3", pt: 0.75 }, autoPage: false, valign: "middle" });
s.addText("Groupes conservés tels quels (âge véhicule, puissance/gabarit, conducteurs) : la redondance est assumée, l'importance se lit au niveau du bloc, pas variable par variable.", {
  x: 0.7, y: 3.75, w: 5.8, h: 1.1, fontFace: THEME.bodyFontFace, fontSize: 12, italic: true, color: SLATE, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2,
});

s.addText("Modèle sévérité (montant) — 2 variables sur 9+", { x: 6.85, y: 1.4, w: 5.8, h: 0.4, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
const sevRows = [
  [{ text: "Constat", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } }, { text: "Conséquence", options: { bold: true, color: "FFFFFF", fill: { color: NAVY } } }],
  ["Spearman max |ρ| = 0,085 (ancienneté véhicule)", "Signal numérique trop faible pour discriminer les variables entre elles"],
  ["8 catégorielles sur 8 non significatives sauf type_contrat (Kruskal-Wallis)", "Pas de variable catégorielle additionnelle à ajouter"],
  ["10 configurations testées (CV 5×3) : écarts de RMSE ≈ 14 €, std ≈ 150 €", "Tous les modèles/jeux de variables sont statistiquement équivalents"],
].map((r, i) => (i === 0 ? r : r.map((t, j) => ({ text: t, options: { color: NAVY, fontSize: 11.5, fill: { color: i % 2 === 0 ? CARD_BG : "FFFFFF" }, bold: j === 0 } }))));
s.addTable(sevRows, { x: 6.85, y: 1.85, w: 5.8, h: 3.0, colW: [2.8, 3.0], fontFace: THEME.bodyFontFace, fontSize: 11.5, border: { type: "solid", color: "D9E2F3", pt: 0.75 }, autoPage: false, valign: "middle" });
s.addText("→ Choix volontairement minimal : maxi (garantie du contrat) + anciennete_vehicule, sans perte de performance mesurable.", {
  x: 6.85, y: 5.0, w: 5.8, h: 0.8, fontFace: THEME.bodyFontFace, fontSize: 12.5, italic: true, color: AMBER2, bold: true, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2,
});

// Slide 11 — Entraînement & choix de modèle
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Choix des variables & modélisation" });
s.addText("Entraînement et choix de modèle", { placeholder: "title" });
s.addShape("roundRect", { x: 0.7, y: 1.45, w: 5.75, h: 5.5, rectRadius: 0.1, fill: { color: CARD_BG }, line: { type: "none" } });
s.addText("Fréquence — Random Forest", { x: 1.0, y: 1.7, w: 5.2, h: 0.45, fontFace: THEME.headFontFace, fontSize: 16, bold: true, color: NAVY, isTextBox: true, margin: 0 });
s.addText(
  [
    { text: "Grille de recherche sur min_samples_leaf × max_features (10 configs)", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "leaf=50 : AUC dev 0,6665 mais écart train-dev 0,1517 (surapprentissage)", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "leaf=200 retenu : AUC dev 0,6643, écart train-dev 0,0423 — meilleur compromis", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Suppression successive de variables validée sur le dev : 17→15 variables, coût −0,0014 AUC seulement", options: { bullet: true, breakLine: true } },
  ],
  { x: 1.0, y: 2.3, w: 5.2, h: 4.4, fontFace: THEME.bodyFontFace, fontSize: 13, color: NAVY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2 }
);
s.addShape("roundRect", { x: 6.85, y: 1.45, w: 5.75, h: 5.5, rectRadius: 0.1, fill: { color: CARD_BG }, line: { type: "none" } });
s.addText("Sévérité — XGBoost", { x: 7.15, y: 1.7, w: 5.2, h: 0.45, fontFace: THEME.headFontFace, fontSize: 16, bold: true, color: NAVY, isTextBox: true, margin: 0 });
s.addText(
  [
    { text: "Comparaison de 8 familles de modèles × jeux de variables (CV RepeatedKFold 5×3)", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Meilleur modèle (RF étendu) : RMSE 1442 € — gain de 0,97 % sur la moyenne naïve", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "Écarts entre modèles (~14 €) dominés par l'écart-type de la CV (~150 €)", options: { bullet: true, breakLine: true, paraSpaceAfter: 8 } },
    { text: "XGBoost (n_estim=100, lr=0,03, depth=3) retenu sur 2 variables — simplicité, sans perte", options: { bullet: true, breakLine: true } },
  ],
  { x: 7.15, y: 2.3, w: 5.2, h: 4.4, fontFace: THEME.bodyFontFace, fontSize: 13, color: NAVY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.2 }
);

// Slide 12 — Résultats & performance
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Choix des variables & modélisation" });
s.addText("Résultats et performance (jeu de test)", { placeholder: "title" });
s.addText("Modèle fréquence", { x: 0.7, y: 1.35, w: 5.0, h: 0.4, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
statCard(s, 0.7, 1.8, 2.75, 1.75, "0,629", "ROC AUC (naïf 0,500)", NAVY);
statCard(s, 3.6, 1.8, 2.75, 1.75, "0,085", "PR AUC (naïf 0,058)", NAVY);
statCard(s, 0.7, 3.7, 2.75, 1.75, "43,5 %", "des sinistres captés dans les 30 % les plus risqués", AMBER2);
statCard(s, 3.6, 3.7, 2.75, 1.75, "0,0544", "Brier score (naïf 0,0550)", NAVY);

s.addText("Modèle sévérité", { x: 6.95, y: 1.35, w: 5.0, h: 0.4, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: NAVY, isTextBox: true, margin: 0 });
statCard(s, 6.95, 1.8, 2.75, 1.75, "1 478 €", "RMSE test (naïf 1 491 €)", NAVY);
statCard(s, 9.85, 1.8, 2.75, 1.75, "0,017", "R² test", NAVY);
statCard(s, 6.95, 3.7, 2.75, 1.75, "103 €", "prime pure moyenne (test)", AMBER2);
statCard(s, 9.85, 3.7, 2.75, 1.75, "1 671 €", "montant attendu moyen prédit", NAVY);

s.addText(
  "Performances modestes en absolu — cohérent avec des associations faibles mesurées en amont (phase 2). Le choix des variables, validé par l'analyse d'association, permet d'atteindre cette performance avec un modèle simple et robuste.",
  { x: 0.7, y: 5.75, w: 11.9, h: 1.1, fontFace: THEME.bodyFontFace, fontSize: 13.5, italic: true, color: BLUE2, isTextBox: true, margin: 0, lineSpacingMultiple: 1.25 }
);

// =====================================================================
// SECTION 4 — Conclusion
// =====================================================================
pres.addSection({ title: "Conclusion" });

// Slide 13 — Limites & améliorations
s = pres.addSlide({ masterName: "CONTENT_LIGHT", sectionTitle: "Conclusion" });
s.addText("Limites et pistes d'amélioration", { placeholder: "title" });
const limits = [
  { t: "Signal faible", d: "Associations maximales modestes (|ρ| ≤ 0,085 côté sévérité) : la marge de progression dépend surtout de nouvelles données." },
  { t: "Petit échantillon test", d: "≈ 290 sinistrés dans le test fréquence : l'écart dev→test (0,664 → 0,629) n'est pas quantifié par un intervalle de confiance." },
  { t: "Redondance non résolue en profondeur", d: "Les blocs corrélés sont gérés par le choix de modèle (RF, XGBoost), pas supprimés — une régression pénalisée (Ridge/Lasso) n'a pas été testée." },
  { t: "Données externes", d: "Historique de sinistres, données socio-démographiques ou météorologiques pourraient renforcer le signal sur les deux cibles." },
];
limits.forEach((l, i) => {
  const col = i % 2, row = Math.floor(i / 2);
  const x = 0.7 + col * 6.1, y = 1.55 + row * 2.75;
  s.addShape("roundRect", { x, y, w: 5.8, h: 2.5, rectRadius: 0.1, fill: { color: CARD_BG }, line: { type: "none" } });
  s.addText(l.t, { x: x + 0.3, y: y + 0.22, w: 5.2, h: 0.5, fontFace: THEME.headFontFace, fontSize: 15, bold: true, color: AMBER2, isTextBox: true, margin: 0 });
  s.addText(l.d, { x: x + 0.3, y: y + 0.78, w: 5.2, h: 1.55, fontFace: THEME.bodyFontFace, fontSize: 12.5, color: NAVY, isTextBox: true, margin: 0, lineSpacingMultiple: 1.25 });
});

// Slide 14 — Conclusion (dark)
s = pres.addSlide({ masterName: "TITLE_DARK", sectionTitle: "Conclusion" });
s.addText("Choisir les variables, c'est déjà choisir le modèle", { placeholder: "title" });
s.addText("L'analyse d'association entre variables explicatives a directement guidé la sélection des variables des deux modèles de pricing.", { placeholder: "body" });
s.addShape("line", { x: 0.9, y: 2.5, w: 1.3, h: 0, line: { color: AMBER, width: 3 } });
const concl = [
  { v: "15 / 17", l: "variables fréquence, justifiées par la permutation groupée" },
  { v: "2 / 9+", l: "variables sévérité, justifiées par l'équivalence statistique des modèles" },
];
concl.forEach((c, i) => statCard(s, 0.9 + i * 4.0, 5.15, 3.7, 1.7, c.v, c.l, NAVY));

// =====================================================================
// Write file + apply theme
// =====================================================================
(async () => {
  await pres.writeFile({ fileName: OUT });
  const { applyTheme } = require("C:/Users/papam/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/7ea41e66-e024-4942-8bc3-6e733925f918/eaca7937-eab9-4673-a247-b00bc31cca59/skills/pptx/scripts/apply_theme.js");
  await applyTheme(OUT, THEME);
  console.log("Deck written to", OUT);
})();
