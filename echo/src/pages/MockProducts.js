const mockProducts = [
    {
        "product_id": "SRM001",
        "name": "Radiant Renewal Serum",
        "category": "Serum",
        "description": "Brightens dull skin and smooths fine lines for a lit-from-within glow.",
        "top_ingredients": "Ascorbic Acid (Vitamin C); Hyaluronic Acid; Niacinamide",
        "tags": "antiaging|brightening|hydration",
        "usd_price": 72.0,
        "margin": 0.48
    },
    {
        "product_id": "SRM002",
        "name": "Dewdrop Hydration Elixir",
        "category": "Serum",
        "description": "Water-weight serum that drenches skin in long-lasting moisture and repairs the barrier.",
        "top_ingredients": "Hyaluronic Acid; Panthenol; Vitamin F (Linoleic Acid)",
        "tags": "hydration|barrier-repair|dry-skin",
        "usd_price": 58.0,
        "margin": 0.42
    },
    {
        "product_id": "SRM003",
        "name": "Clear Slate BHA Serum",
        "category": "Serum",
        "description": "Clarifies congested pores and keeps oil in check without over-drying.",
        "top_ingredients": "Salicylic Acid; Zinc PCA; Green-Tea Extract",
        "tags": "acne-prone|oily-control|pore-care",
        "usd_price": 46.0,
        "margin": 0.4
    },
    {
        "product_id": "SRM004",
        "name": "Midnight Peptide Firming Serum",
        "category": "Serum",
        "description": "Overnight peptide complex visibly firms and nourishes mature skin.",
        "top_ingredients": "Palmitoyl Tripeptide-5; Soluble Collagen; Vitamin E",
        "tags": "antiaging|firming|dry-skin",
        "usd_price": 85.0,
        "margin": 0.52
    },
    {
        "product_id": "SRM005",
        "name": "Calm & Soothe Sensitive Serum",
        "category": "Serum",
        "description": "Lightweight gel serum that calms redness and strengthens sensitive skin.",
        "top_ingredients": "Centella Asiatica; Allantoin; Beta-Glucan",
        "tags": "sensitive|redness-relief|hydration",
        "usd_price": 49.0,
        "margin": 0.38
    },
    {
        "product_id": "SRM006",
        "name": "Flash Fade Spot Corrector",
        "category": "Serum",
        "description": "Targets dark spots and post-acne marks for an even, luminous tone.",
        "top_ingredients": "Tranexamic Acid; Niacinamide; Licorice-Root Extract",
        "tags": "brightening|antiaging|hyperpigmentation",
        "usd_price": 79.0,
        "margin": 0.5
    },
    {
        "product_id": "SRM007",
        "name": "Velvet Matte Pore Serum",
        "category": "Serum",
        "description": "Blurs shine and minimizes pores for a soft-focus finish.",
        "top_ingredients": "Niacinamide; Tremella Mushroom Extract; Willow-Bark",
        "tags": "oily-skin|pore-refining|matte",
        "usd_price": 54.0,
        "margin": 0.41
    },
    {
        "product_id": "SRM008",
        "name": "AquaShield Barrier Booster",
        "category": "Serum",
        "description": "Ceramide-rich serum that reinforces the lipid barrier and locks in moisture.",
        "top_ingredients": "Ceramides NP+AP+EOP; Vitamin F; Squalane",
        "tags": "hydration|barrier-repair|dry-skin",
        "usd_price": 65.0,
        "margin": 0.44
    },
    {
        "product_id": "SRM009",
        "name": "Sunrise Retinal Serum",
        "category": "Serum",
        "description": "Next-gen retinaldehyde visibly smooths wrinkles with less irritation.",
        "top_ingredients": "Retinaldehyde; Bakuchiol; Hyaluronic Acid",
        "tags": "antiaging|fine-lines|brightening",
        "usd_price": 95.0,
        "margin": 0.55
    },
    {
        "product_id": "SRM010",
        "name": "Glow Guard Antioxidant Serum",
        "category": "Serum",
        "description": "Potent antioxidant trio defends against pollution and UV stress.",
        "top_ingredients": "Ferulic Acid; Ascorbic Acid (Vit C); Vitamin E",
        "tags": "antioxidant|brightening|antiaging",
        "usd_price": 82.0,
        "margin": 0.47
    },
    {
        "product_id": "TNR001",
        "name": "Rosewater Rescue Hydrating Toner",
        "category": "Toner",
        "description": "Alcohol-free rosewater blend that replenishes moisture and soothes tight, very-dry skin.",
        "top_ingredients": "Damask Rose Water; Glycerin; Aloe Vera Juice",
        "tags": "hydration|very-dry|sensitive|natural",
        "usd_price": 32.0,
        "margin": 0.4
    },
    {
        "product_id": "TNR002",
        "name": "ClearWave 2% BHA Toner",
        "category": "Toner",
        "description": "Oil-controlling liquid exfoliant unclogs pores and keeps breakouts at bay for oily, acne-prone skin.",
        "top_ingredients": "Salicylic Acid 2%; Witch Hazel; Niacinamide",
        "tags": "oily|acne-prone|pore-care|BHA",
        "usd_price": 38.0,
        "margin": 0.45
    },
    {
        "product_id": "TNR003",
        "name": "GlowPrep 5% Glycolic Toner",
        "category": "Toner",
        "description": "Daily AHA toner that sweeps away dull cells and brightens uneven tone.",
        "top_ingredients": "Glycolic Acid 5%; Lactic Acid; Rooibos Extract",
        "tags": "AHA|brightening|combo-skin",
        "usd_price": 42.0,
        "margin": 0.47
    },
    {
        "product_id": "TNR004",
        "name": "CalmCucumber pH Mist",
        "category": "Toner",
        "description": "Ultra-gentle mist balances pH and calms redness—ideal for reactive or sensitized skin.",
        "top_ingredients": "Cucumber Water; Allantoin; Panthenol",
        "tags": "sensitive|redness-relief|natural|hydration",
        "usd_price": 28.0,
        "margin": 0.36
    },
    {
        "product_id": "TNR005",
        "name": "SmoothStart PHA Tonic",
        "category": "Toner",
        "description": "Mild polyhydroxy toner refines texture without irritation—great for combination or first-time exfoliators.",
        "top_ingredients": "Gluconolactone (PHA); Green Tea Extract; Hyaluronic Acid",
        "tags": "combo-skin|gentle-exfoliation|PHA",
        "usd_price": 35.0,
        "margin": 0.42
    },
    {
        "product_id": "CRM001",
        "name": "HydraCloud Daily Gel-Cream SPF 30",
        "category": "Sunscreen",
        "description": "Weightless water-gel that floods skin with moisture while protecting against UVA/UVB.",
        "top_ingredients": "Hyaluronic Acid; Niacinamide; Zinc Oxide (SPF 30)",
        "tags": "hydration|SPF|day-cream|combo-skin",
        "usd_price": 42.0,
        "margin": 0.4
    },
    {
        "product_id": "CRM002",
        "name": "Velvet Night Repair Cream",
        "category": "Cream / Moisturizer",
        "description": "Luxurious overnight treatment that boosts collagen and repairs the skin barrier while you sleep.",
        "top_ingredients": "Retinol; Peptides; Squalane",
        "tags": "night-repair|antiaging|dry-skin",
        "usd_price": 68.0,
        "margin": 0.48
    },
    {
        "product_id": "CRM003",
        "name": "Radiance Spot-Bright Eye Cream",
        "category": "Cream / Moisturizer",
        "description": "Brightens dark circles and smooths fine lines around delicate eye area.",
        "top_ingredients": "Vitamin C; Caffeine; Niacinamide",
        "tags": "eye-care|brightening|antiaging|hydration",
        "usd_price": 55.0,
        "margin": 0.46
    },
    {
        "product_id": "CRM004",
        "name": "Deep Nourish Body Butter",
        "category": "Cream / Moisturizer",
        "description": "Ultra-rich whipped butter that melts into skin for 24-hour nourishment.",
        "top_ingredients": "Shea Butter; Cocoa Butter; Vitamin E",
        "tags": "body|very-dry|hydration|natural",
        "usd_price": 38.0,
        "margin": 0.35
    },
    {
        "product_id": "CRM005",
        "name": "SmoothLift Wrinkle Corrector",
        "category": "Cream / Moisturizer",
        "description": "Targeted wrinkle-filler cream visibly softens lines and plumps skin.",
        "top_ingredients": "Palmitoyl Tripeptide-1; Hyaluronic Acid; Bakuchiol",
        "tags": "wrinkle-care|antiaging|plumping",
        "usd_price": 85.0,
        "margin": 0.52
    },
    {
        "product_id": "CRM006",
        "name": "BarrierFix Ceramide Cream",
        "category": "Cream / Moisturizer",
        "description": "Ceramide-packed cream that restores a compromised skin barrier and calms redness.",
        "top_ingredients": "Ceramides NP+AP+EOP; Panthenol; Cholesterol",
        "tags": "barrier-repair|sensitive|hydration",
        "usd_price": 62.0,
        "margin": 0.44
    },
    {
        "product_id": "CRM007",
        "name": "ClearMatte Oil-Control Gel Moisturizer",
        "category": "Cream / Moisturizer",
        "description": "Lightweight gel absorbs instantly, controls shine, and keeps pores clear.",
        "top_ingredients": "Niacinamide; Green-Tea Extract; Willow-Bark",
        "tags": "oily-skin|acne-prone|matte|hydration",
        "usd_price": 48.0,
        "margin": 0.38
    },
    {
        "product_id": "CRM008",
        "name": "SunShield Mineral Moisturizer SPF 50",
        "category": "Cream / Moisturizer",
        "description": "Broad-spectrum mineral sunscreen meets daily moisturizer for outdoor days.",
        "top_ingredients": "Titanium Dioxide; Zinc Oxide (SPF 50); Aloe Vera",
        "tags": "SPF|protection|sensitive|day-cream",
        "usd_price": 58.0,
        "margin": 0.45
    },
    {
        "product_id": "CRM009",
        "name": "Arctic Hand Rescue Cream",
        "category": "Cream / Moisturizer",
        "description": "Intense hand cream that repairs cracks and shields against harsh cold.",
        "top_ingredients": "Glycerin; Arctic Oat Lipids; Allantoin",
        "tags": "hand-care|very-dry|repair|natural",
        "usd_price": 29.0,
        "margin": 0.37
    },
    {
        "product_id": "CRM010",
        "name": "Glow Fade Dark-Spot Moisturizer",
        "category": "Cream / Moisturizer",
        "description": "Daily brightening cream that gradually fades discoloration while hydrating.",
        "top_ingredients": "Tranexamic Acid; Alpha-Arbutin; Licorice Root",
        "tags": "spot-corrector|brightening|hydration|antiaging",
        "usd_price": 72.0,
        "margin": 0.48
    },
    {
        "product_id": "SNS001",
        "name": "SunVeil Ultra-Light Fluid SPF 50",
        "category": "Cream / Moisturizer",
        "description": "Feather-weight sunscreen fluid that sinks in instantly, leaving zero white cast and a soft-matte finish.",
        "top_ingredients": "Zinc Oxide (SPF 50); Vitamin E; Helichrysum Extract",
        "tags": "SPF|protection|oil-free|sensitive-skin",
        "usd_price": 48.0,
        "margin": 0.46
    },
    {
        "product_id": "MSK001",
        "name": "HydraDream Overnight Mask",
        "category": "Face Mask",
        "description": "Cushiony sleeping mask that seals in moisture and plumps skin while you rest.",
        "top_ingredients": "Hyaluronic Acid; Ceramides; Blue Agave Ferment",
        "tags": "overnight|hydration|plumping|dry-skin",
        "usd_price": 58.0,
        "margin": 0.49
    },
    {
        "product_id": "MSK002",
        "name": "Clarify Clay Rinse-Off Mask",
        "category": "Face Mask",
        "description": "Detox clay mask that vacuums pores and reduces excess oil in ten minutes.",
        "top_ingredients": "Kaolin Clay; Charcoal; Salicylic Acid",
        "tags": "rinse-off|clarifying|oily-skin|pore-care",
        "usd_price": 42.0,
        "margin": 0.4
    },
    {
        "product_id": "MSK003",
        "name": "Flash Glow AHA Peel Mask",
        "category": "Face Mask",
        "description": "5-minute rinse-off jelly mask that resurfaces for glassy radiance.",
        "top_ingredients": "Glycolic Acid 10%; Papaya Enzyme; Niacinamide",
        "tags": "rinse-off|brightening|AHA|dull-skin",
        "usd_price": 52.0,
        "margin": 0.45
    },
    {
        "product_id": "BW001",
        "name": "Revive Citrus Shower Gel",
        "category": "Body Wash",
        "description": "Sulphate-free body wash with energizing citrus aroma and silky lather.",
        "top_ingredients": "Vitamin C; Orange Essential Oil; Aloe Vera",
        "tags": "body-wash|energizing|sulfate-free|aromatic",
        "usd_price": 25.0,
        "margin": 0.34
    },
    {
        "product_id": "BW002",
        "name": "Soothe & Silk Sensitive Wash",
        "category": "Body Wash",
        "description": "Ultra-gentle wash that calms itchy, reactive skin while cleansing.",
        "top_ingredients": "Colloidal Oat; Allantoin; Chamomile Extract",
        "tags": "body-wash|sensitive|fragrance-free|soothing",
        "usd_price": 28.0,
        "margin": 0.35
    },
    {
        "product_id": "BW003",
        "name": "Polish Glow Exfoliating Body Wash",
        "category": "Body Wash",
        "description": "Dual-action body wash with micro-pumice for smooth, luminous skin.",
        "top_ingredients": "Lactic Acid; Bamboo Powder; Rice Bran Oil",
        "tags": "body-wash|exfoliating|brightening|AHA",
        "usd_price": 30.0,
        "margin": 0.36
    },
    {
        "product_id": "HC001",
        "name": "SleekSilk Anti-Frizz Shampoo",
        "category": "Shampoo",
        "description": "Sulfate-free cleanser that smooths flyaways and adds glassy shine.",
        "top_ingredients": "Argan Oil; Hydrolyzed Keratin; Panthenol",
        "tags": "shampoo|frizz-control|sulfate-free|shine",
        "usd_price": 24.0,
        "margin": 0.38
    },
    {
        "product_id": "HC002",
        "name": "ScalpBalance Anti-Dandruff Shampoo",
        "category": "Shampoo",
        "description": "Gentle yet effective shampoo that clears flakes without over-drying.",
        "top_ingredients": "Pyrithione Zinc 1%; Tea Tree Oil; Salicylic Acid",
        "tags": "shampoo|dandruff|oily-scalp|soothing",
        "usd_price": 26.0,
        "margin": 0.4
    },
    {
        "product_id": "HC003",
        "name": "ColorLock Vibrant-Hue Shampoo",
        "category": "Shampoo",
        "description": "Protects color vibrancy and shields from UV fade for dyed hair.",
        "top_ingredients": "Quinoa Protein; UV Filter; Hibiscus Extract",
        "tags": "shampoo|color-protection|sulfate-free",
        "usd_price": 28.0,
        "margin": 0.41
    },
    {
        "product_id": "HC004",
        "name": "SleekSilk Anti-Frizz Conditioner",
        "category": "Conditioner",
        "description": "Rich conditioner that seals cuticles and tames frizz for silkier strands.",
        "top_ingredients": "Argan Oil; Shea Butter; Cetearyl Alcohol",
        "tags": "conditioner|frizz-control|shine",
        "usd_price": 26.0,
        "margin": 0.38
    },
    {
        "product_id": "HC005",
        "name": "FeatherLight Oil-Balance Conditioner",
        "category": "Conditioner",
        "description": "Weightless conditioner that hydrates ends without weighing down oily scalps.",
        "top_ingredients": "Rice Water; Niacinamide; Aloe Vera",
        "tags": "conditioner|oily-scalp|lightweight|silicone-free",
        "usd_price": 25.0,
        "margin": 0.37
    },
    {
        "product_id": "HC006",
        "name": "ColorLock Vibrant-Hue Conditioner",
        "category": "Conditioner",
        "description": "Color-safe conditioner that boosts vibrancy and prevents hue stripping.",
        "top_ingredients": "Quinoa Protein; Sunflower Seed Oil; Vitamin E",
        "tags": "conditioner|color-protection|UV-shield",
        "usd_price": 30.0,
        "margin": 0.41
    },
    {
        "product_id": "HC007",
        "name": "RepairRitual Deep Mask (Silicone-Free)",
        "category": "Hair Mask",
        "description": "Weekly mask that mends split ends and strengthens over-processed hair—no silicones or parabens.",
        "top_ingredients": "Hydrolyzed Silk Protein; Ceramides; Avocado Oil",
        "tags": "hair-mask|repair|no-silicones|no-parabens",
        "usd_price": 32.0,
        "margin": 0.45
    }
]

export default mockProducts