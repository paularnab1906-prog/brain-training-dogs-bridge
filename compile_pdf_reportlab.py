import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        # Don't draw headers/footers on cover page
        if self._pageNumber == 1:
            return
        
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#524e4a"))
        
        # Header
        self.drawString(54, 750, "The Smart Dog Starter Kit — 5 Brain Games Guide")
        self.setStrokeColor(colors.HexColor("#e1dedb"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.drawString(54, 40, "© 2026 Smart Paw Tips — smartpawtips.com")
        self.line(54, 52, 558, 52)
        
        self.restoreState()

def build_pdf():
    project_dir = r"c:\Users\Code\AppData\Roaming\Open Design\namespaces\release-stable-win\data\projects\3ab3cb91-97c1-41d4-8376-ae2da6373727"
    pdf_path = os.path.join(project_dir, "Smart-Dog-Starter-Kit-5-Brain-Games.pdf")
    cover_image_path = os.path.join(project_dir, "lead-magnet-cover-golden-retriever-snuffle-mat.png")
    
    # 54pt margin = 0.75 inch
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom styles
    primary_color = colors.HexColor("#3a7d56") # var(--accent-dark)
    secondary_color = colors.HexColor("#4a9d6c") # var(--accent)
    text_color = colors.HexColor("#2d2926") # var(--fg)
    muted_color = colors.HexColor("#7a7570") # var(--muted)
    light_bg = colors.HexColor("#f8f6f4") # var(--warm)
    border_color = colors.HexColor("#e8e5e2") # var(--border)
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=text_color,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=muted_color,
        alignment=1, # Center
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'HeadingPrimary',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceBefore=22,
        spaceAfter=12,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'HeadingSecondary',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=text_color,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=16,
        textColor=text_color,
        spaceAfter=10
    )
    
    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=primary_color,
        spaceAfter=8
    )

    tip_style = ParagraphStyle(
        'TipText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=text_color
    )
    
    sig_style = ParagraphStyle(
        'Signature',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=16,
        textColor=primary_color,
        spaceAfter=15
    )
    
    story = []
    
    # ------------------ PAGE 1: COVER PAGE ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("FREE PDF GUIDE &middot; FOR DOG OWNERS", ParagraphStyle('CoverBadge', fontName='Helvetica-Bold', fontSize=9, textColor=primary_color, alignment=1, spaceAfter=20)))
    story.append(Paragraph("The Smart Dog Starter Kit", title_style))
    story.append(Paragraph("5 Free 5-Minute Brain Games for Better Focus and Engagement", subtitle_style))
    
    # Cover Image
    if os.path.exists(cover_image_path):
        story.append(Image(cover_image_path, width=4.5*inch, height=3.375*inch))
        story.append(Spacer(1, 30))
    else:
        story.append(Spacer(1, 150))
        
    story.append(Paragraph("Smart Paw Tips", ParagraphStyle('CoverAuthor', fontName='Helvetica-Bold', fontSize=12, textColor=text_color, alignment=1, spaceAfter=4)))
    story.append(Paragraph("Evidence-Based Mental Enrichment for Your Dog", ParagraphStyle('CoverAuthorSub', fontName='Helvetica', fontSize=10, textColor=muted_color, alignment=1)))
    story.append(PageBreak())
    
    # ------------------ PAGE 2: INTRO & SCIENCE ------------------
    story.append(Paragraph("Introduction", h1_style))
    story.append(Paragraph("Here's the thing most dog owners never hear from their vet: <b>most \"bad behavior\" in dogs isn't a behavior problem at all — it's a boredom problem.</b>", body_style))
    story.append(Paragraph("Chewing your shoes, barking at nothing, digging up the yard, pulling on the leash — these aren't signs of a \"bad dog.\" They're signs of a smart dog with nothing to think about.", body_style))
    story.append(Paragraph("This guide gives you 5 brain games that take less than 5 minutes each. They're based on the same principles used in clinical animal behavior practice — and every single one is free. No expensive toys to buy. No complex equipment to set up.", body_style))
    story.append(Paragraph("Let's get your dog thinking.", sig_style))
    
    story.append(Paragraph("Why Brain Games Actually Work", h1_style))
    story.append(Paragraph("The mechanism is straightforward. Dogs evolved as scavengers and problem-solvers. Their brains are wired to search, hunt, figure out, and work for food. When we take away that mental work — feed them from a bowl twice a day, give them a yard to lie in — we leave a cognitive engine idling with nothing to do.", body_style))
    story.append(Paragraph("That energy doesn't just disappear. It redirects. A 2019 study from the University of Lincoln's Animal Behavior Clinic found that dogs with lower daily mental stimulation showed significantly more stress-related behaviors — excessive vocalization, destructive chewing, and restlessness.", body_style))
    
    # Science Highlight Box
    science_box_text = Paragraph("<b>The fix isn't more exercise.</b> It's more <i>thinking.</i> A 10-minute brain game tires a dog out more than a 30-minute walk, because it engages the neural circuits they're starving to use. Veterinary behaviorists call this \"cognitive enrichment\" — and it's now a standard recommendation for behavior modification alongside training.", body_style)
    science_table = Table([[science_box_text]], colWidths=[5.0*inch])
    science_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), light_bg),
        ('PADDING', (0,0), (-1,-1), 12),
        ('LINELEFT', (0,0), (0,-1), 4, primary_color),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(science_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph("Each game below targets a different cognitive skill: scent work, impulse control, spatial reasoning, memory, and problem-solving. Together, they give your dog the full \"mental workout\" that keeps their brain satisfied and your furniture intact.", body_style))
    story.append(PageBreak())
    
    # Helper to format games
    def add_game(num, title, difficulty, time, category, why, desc, steps, tip=None, warning=None, level_up=None):
        elements = []
        elements.append(Paragraph(f"Game {num}: {title}", h2_style))
        elements.append(Paragraph(f"DIFFICULTY: {difficulty}  |  TIME: {time}  |  TYPE: {category}", meta_style))
        
        # Why it works block
        why_para = Paragraph(f"<b>Why it works:</b> {why}", body_style)
        why_table = Table([[why_para]], colWidths=[5.0*inch])
        why_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), light_bg),
            ('PADDING', (0,0), (-1,-1), 8),
            ('LINELEFT', (0,0), (0,-1), 3, secondary_color),
        ]))
        elements.append(why_table)
        elements.append(Spacer(1, 8))
        
        elements.append(Paragraph(desc, body_style))
        
        # Steps
        elements.append(Paragraph("<b>How to play:</b>", ParagraphStyle('StepsHeader', parent=body_style, fontName='Helvetica-Bold', spaceAfter=4)))
        for i, step in enumerate(steps, 1):
            elements.append(Paragraph(f"{i}. {step}", ParagraphStyle('StepItem', parent=body_style, leftIndent=15, firstLineIndent=-15, spaceAfter=4)))
        
        elements.append(Spacer(1, 6))
        
        if tip:
            tip_para = Paragraph(f"<b>Pro Tip:</b> {tip}", tip_style)
            tip_table = Table([[tip_para]], colWidths=[5.0*inch])
            tip_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fbfbfa")),
                ('PADDING', (0,0), (-1,-1), 8),
                ('LINELEFT', (0,0), (0,-1), 3, primary_color),
                ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ]))
            elements.append(tip_table)
            elements.append(Spacer(1, 6))
            
        if level_up:
            l_para = Paragraph(f"<b>Level Up:</b> {level_up}", tip_style)
            l_table = Table([[l_para]], colWidths=[5.0*inch])
            l_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#fbfbfa")),
                ('PADDING', (0,0), (-1,-1), 8),
                ('LINELEFT', (0,0), (0,-1), 3, colors.HexColor("#4a8db0")),
                ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ]))
            elements.append(l_table)
            elements.append(Spacer(1, 6))
            
        if warning:
            w_para = Paragraph(f"<b>Important Warning:</b> {warning}", ParagraphStyle('WarningStyle', parent=tip_style, textColor=colors.HexColor("#a83232")))
            w_table = Table([[w_para]], colWidths=[5.0*inch])
            w_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#faf5f5")),
                ('PADDING', (0,0), (-1,-1), 8),
                ('LINELEFT', (0,0), (0,-1), 3, colors.HexColor("#a83232")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#ebd6d6")),
            ]))
            elements.append(w_table)
            elements.append(Spacer(1, 6))
            
        elements.append(Spacer(1, 15))
        return elements

    # ------------------ PAGE 3: GAMES 1 & 2 ------------------
    story.append(Paragraph("The 5 Enrichment Games", h1_style))
    
    # Game 1
    g1 = add_game(
        num=1,
        title="The Muffin Tin Game",
        difficulty="Beginner",
        time="5 minutes",
        category="Scent + Foraging",
        why="Taps into your dog's 300-million-year-old foraging instinct. The olfactory engagement alone lowers heart rate and cortisol levels.",
        desc="This is the gateway game. It teaches your dog to use their nose instead of their mouth to solve problems — which directly redirects destructive chewing into constructive thinking.",
        steps=[
            "Grab a 6-cup muffin tin (the standard kind you'd use for cupcakes).",
            "Place a treat in <b>3 of the 6 cups</b>. Use smelly treats — freeze-dried liver works great, or a bit of cheese.",
            "Cover <b>all 6 cups</b> with tennis balls, crumpled paper balls, or muffin liners.",
            "Set the tin on the floor and let your dog figure it out.",
            "Let them sniff, nudge, and paw at the covers until they find the treats underneath."
        ],
        tip="Don't help them. It's tempting to lift a ball and say 'it's under here!' — but the learning happens in the struggle. If they get frustrated after 2 minutes, remove one ball to reveal a treat, then try again next time.",
        level_up="Once they've got it, switch to a 12-cup tin. Then cover every cup but only put treats in 2 — forcing them to rely on scent, not random searching."
    )
    for el in g1: story.append(el)
    
    story.append(PageBreak())
    
    # Game 2
    g2 = add_game(
        num=2,
        title="The Shell Game",
        difficulty="Intermediate",
        time="5 minutes",
        category="Memory + Visual Tracking",
        why="Builds working memory and impulse control simultaneously. Dogs must hold information (which cup?) while resisting the urge to rush.",
        desc="Made famous by cognitive researchers testing animal memory, this game has been used in university studies on canine cognition. It's simple to set up but surprisingly challenging for your dog's brain.",
        steps=[
            "Sit on the floor facing your dog. Place 3 identical cups (or small buckets) upside-down in a row between you, about 8 inches apart.",
            "Show your dog a treat. Let them smell it.",
            "Slowly place the treat under one cup while they watch.",
            "Say 'Find it!' and let them knock over the cup to get the treat.",
            "Repeat 5 times, always letting them watch you hide the treat.",
            "Now the real test: hide the treat, <b>shuffle the cups slowly</b> (2-3 swaps), then say 'Find it!'",
            "Let them choose. If they pick correctly, they get the treat. If wrong, show them where it was and try again."
        ],
        tip="Shuffle slowly at first. The goal isn't to trick your dog — it's to make them <i>think</i>. Increase speed only when they're consistently correct at the current level.",
        level_up="Add a 4th cup. Or add a 5-second 'wait' delay between shuffling and releasing them — this builds impulse control on top of memory."
    )
    for el in g2: story.append(el)
    
    story.append(PageBreak())
    
    # ------------------ PAGE 4: GAMES 3 & 4 ------------------
    # Game 3
    g3 = add_game(
        num=3,
        title="\"Find It\" — The Scent Trail",
        difficulty="Beginner",
        time="5 minutes",
        category="Olfactory Enrichment",
        why="A dog's nose has 300 million scent receptors (humans have 5 million). Scent work activates the parasympathetic nervous system — it literally calms them at a physiological level.",
        desc="This is the single most calming game on the list. It's used in shelters to reduce anxiety in stressed dogs, and by search-and-rescue trainers to build scent drive. For your dog, it's a quiet, focused activity that ends with them more relaxed than when they started.",
        steps=[
            "Pick a strong-smelling treat: freeze-dried fish, liver, or a dab of peanut butter works well.",
            "Put your dog in a 'stay' or hold them by the collar. Let them watch you place a treat on the floor <b>3 feet away</b> — in plain sight.",
            "Say 'Find it!' and release them. They'll walk over and eat it. Easy.",
            "Repeat, placing the treat further away: 5 feet, then 10 feet, then across the room.",
            "Now place the treat behind a chair leg, under a table, or just out of sight in the room.",
            "Say 'Find it!' and watch them switch from sight to scent to locate it.",
            "Gradually increase difficulty: other rooms, higher surfaces, buried under a towel."
        ],
        tip="Use the same command ('Find it!') every time. Dogs associate the phrase with the action. After a week, you can say 'Find it' with no treat visible and they'll start searching — the behavior itself becomes rewarding.",
        warning="Never hide treats in places your dog needs to destroy to reach them (inside couch cushions, behind drywall). If they start digging or chewing to get to a treat, you've hidden it too well — go back a level."
    )
    for el in g3: story.append(el)
    
    story.append(PageBreak())
    
    # Game 4
    g4 = add_game(
        num=4,
        title="The Towel Puzzle",
        difficulty="Intermediate",
        time="5 minutes",
        category="Problem-Solving + Persistence",
        why="Builds 'frustration tolerance' — the ability to keep trying when something is hard. This is the cognitive skill most linked to calm behavior in dogs.",
        desc="Dogs who chew furniture, bark at doors, or dig at carpets often have low frustration tolerance — they try something briefly, fail, and redirect to destructive behavior. This game teaches them that persistence pays off, and that 'hard' doesn't mean 'give up.'",
        steps=[
            "Lay a bath towel flat on the floor.",
            "Scatter small treats across the center of the towel — about 5-6 pieces.",
            "Fold the towel in half, then fold it again into a small rectangle. The treats are now buried inside the folds.",
            "Place the folded towel in front of your dog and say 'Find it!'",
            "They'll use their nose, paws, and mouth to unfold it and extract the treats.",
            "Let them work. Don't help unless they completely give up after 3+ minutes."
        ],
        tip="Use small, smelly treats that won't fall out when they shake the towel. Freeze-dried minnows or liver bits work perfectly — the scent motivates them even when they can't see the food.",
        level_up="Roll the towel up instead of folding. Then tie it in a loose knot. Each increase in difficulty builds more persistence."
    )
    for el in g4: story.append(el)
    
    story.append(PageBreak())
    
    # ------------------ PAGE 5: GAME 5 & ROUTINES ------------------
    # Game 5
    g5 = add_game(
        num=5,
        title="The Focus Flight Game",
        difficulty="Advanced",
        time="5 minutes",
        category="Object Recognition + Recall",
        why="This is the most cognitively demanding game on the list. It requires your dog to hold a mental representation of an object, retrieve it from memory, and execute a motor plan — essentially, thinking.",
        desc="Border collies and working breeds excel at this, but any dog can learn it. It builds the same 'focused attention' circuits that calm an anxious, scattered mind. Think of it as meditation for your dog — they can't be barking at the mail carrier if they're concentrating on finding 'blue.'",
        steps=[
            "Pick 2 toys your dog already knows — a ball and a stuffed animal works well. Give them clear, distinct names ('Ball' and 'Bear').",
            "Sit on the floor with your dog. Hold both toys.",
            "Say 'Ball' and offer the ball. When they touch or take it, praise and give a treat. Repeat 5 times.",
            "Say 'Bear' and offer the stuffed animal. Praise and treat when they touch it. Repeat 5 times.",
            "Now place both toys on the floor, 2 feet apart. Say 'Ball.' If they go to the ball, big praise and treat. If they go to the wrong one, no treat — just say the correct name and gently guide them.",
            "Repeat until they reliably choose the correct toy 8 out of 10 times.",
            "Add a third toy. Then increase the distance between toys. Then place them in different rooms."
        ],
        tip="Keep sessions short and end on a success. If they get 3 wrong in a row, go back to an easier version. The goal is engagement, not perfection.",
        level_up="Once they know 3+ toy names, add action commands: 'Bear to ball' (take the bear to where the ball is). This chains object recognition with spatial reasoning."
    )
    for el in g5: story.append(el)
    
    story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # ------------------ PAGE 6: SCHEDULES & FAQ ------------------
    story.append(Paragraph("Suggested Daily Routine", h1_style))
    story.append(Paragraph("Pick one game in the morning and one in the evening. Consistency matters more than variety — doing the same game for 3-4 days builds mastery before you switch.", body_style))
    
    # Schedule Table
    sched_data = [
        [Paragraph("<b>Time of Day</b>", body_bold), Paragraph("<b>Enrichment Activity</b>", body_bold)],
        [Paragraph("Morning", body_bold), Paragraph("Game 1 or 3 — before breakfast (hungry = motivated)", body_style)],
        [Paragraph("Midday", body_bold), Paragraph("If possible: Game 2 or 4 — short session while you're home", body_style)],
        [Paragraph("Evening", body_bold), Paragraph("Game 4 or 5 — after dinner, when they're restless", body_style)],
        [Paragraph("Anytime", body_bold), Paragraph("Game 3 (\"Find It\") — perfect for calming before guests arrive or bedtime", body_style)]
    ]
    sched_table = Table(sched_data, colWidths=[1.5*inch, 3.5*inch])
    sched_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(sched_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("7-Day Streak Tracker", h2_style))
    story.append(Paragraph("Mark each day you play at least one brain game with your dog. After 7 days, you'll notice a difference in their behavior — calmer evenings, less destructive chewing, better focus.", body_style))
    
    # Tracker Table (empty checkboxes)
    tracker_data = [
        [Paragraph("<b>Mon</b>", body_bold), Paragraph("<b>Tue</b>", body_bold), Paragraph("<b>Wed</b>", body_bold), Paragraph("<b>Thu</b>", body_bold), Paragraph("<b>Fri</b>", body_bold), Paragraph("<b>Sat</b>", body_bold), Paragraph("<b>Sun</b>", body_bold)],
        ["[  ]", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]", "[  ]"]
    ]
    tracker_table = Table(tracker_data, colWidths=[0.71*inch]*7)
    tracker_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), light_bg),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(tracker_table)
    
    story.append(PageBreak())
    
    # ------------------ PAGE 7: FAQ & CTA ------------------
    story.append(Paragraph("Common Questions", h1_style))
    
    faqs = [
        ("My dog isn't food-motivated. Will these games work?", 
         "Most dogs are food-motivated — they just aren't hungry enough. Play these games before meals, not after. Use higher-value treats than you'd normally give (real chicken, cheese, freeze-dried fish). If your dog truly won't work for food, substitute a favorite toy as the 'treasure' in games 1, 2, and 4."),
        ("My dog is older / has arthritis. Are these safe?", 
         "All 5 games are low-impact — no jumping, no running. Game 3 ('Find It') and Game 1 (Muffin Tin) are especially gentle because they're mostly mental. For arthritic dogs, keep the muffin tin on a low table so they don't have to bend far. Skip Game 5 if your dog has vision issues that make object recognition difficult."),
        ("How long before I see a behavior change?", 
         "Most owners report calmer evenings within 3-5 days of daily brain games. Significant reduction in destructive behavior usually takes 2-3 weeks of consistency. The key word is consistency — one game per day, every day, matters more than marathon sessions on weekends.")
    ]
    
    for q, a in faqs:
        story.append(Paragraph(f"<b>Q: {q}</b>", ParagraphStyle('FAQ_Q', parent=body_style, fontName='Helvetica-Bold', spaceBefore=8)))
        story.append(Paragraph(f"A: {a}", body_style))
        story.append(Spacer(1, 4))
        
    story.append(Spacer(1, 20))
    
    # CTA Box
    cta_header = Paragraph("<b>Ready to Unlock Your Dog's Full Potential?</b>", ParagraphStyle('CTAHeader', fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.white, alignment=1))
    cta_body = Paragraph("These 5 games are just the beginning. The full <b>Brain Training for Dogs</b> program includes 21+ games, structured difficulty modules from beginner to advanced, and step-by-step video lessons for every exercise.", ParagraphStyle('CTABody', fontName='Helvetica', fontSize=9.5, leading=14, textColor=colors.white, alignment=1))
    cta_link = Paragraph("<b><font color='#ffffff'><u>Get the Full 21-Game Program Here &rarr;</u></font></b>", ParagraphStyle('CTALink', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.white, alignment=1, spaceBefore=8))
    
    cta_cell = [cta_header, Spacer(1, 8), cta_body, Spacer(1, 4), cta_link]
    cta_table = Table([[cta_cell]], colWidths=[5.0*inch])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary_color),
        ('PADDING', (0,0), (-1,-1), 16),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 16),
    ]))
    
    # Wrap in Link
    # Note: ReportLab doesn't support href on whole tables, but we can set href inside Paragraphs using a link tag
    # Let's adjust the cta_link paragraph to have a ClickBank hoplink:
    hoplink = "https://b5ffe3vcm3ls9la8u3qmc3r6uh.hop.clickbank.net"
    cta_link_with_href = Paragraph(f"<a href='{hoplink}'><b><font color='#ffffff'><u>Get the Full 21-Game Program Here &rarr;</u></font></b></a>", ParagraphStyle('CTALink', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=colors.white, alignment=1, spaceBefore=8))
    cta_cell[4] = cta_link_with_href
    
    story.append(cta_table)
    
    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF compilation completed successfully via ReportLab!")

if __name__ == "__main__":
    build_pdf()
