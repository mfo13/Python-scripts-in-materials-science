"""
Simplified derivation of Schrödinger's equations

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It produces a mp4 movie for the simplified derivation of the
Schrödinger's equations with visual effects of the Manim library 

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for undergrad students.

Packages needed:
manim
ps.: must have Latex in your system

Usage:
$ python derivation_schrodinger.py

You can choose between english or portuguese (Brazil)
by setting the variable 'lang' in the #Main

Date: July/2024
Version: 1.0
"""

# import the library
from manim import *

# we define the scene class
class SchrodingerPresentation(Scene):

    # contruction of parts or slides
    def construct(self):
        
        # Slide 1: Title Slide
        self.title_slide()
        
        # Slide 2
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_2()
    
        # Slide 3
        self.wait(3)  
        self.remove(*self.mobjects)
        self.slide_3()
        
        # Slide 4
        self.wait(3) 
        self.remove(*self.mobjects)
        self.slide_4()
        
        # Slide 5
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_5()
        
        # Slide 6
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_6()
        
        # Slide 7
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_7()
        
        # Slide 8
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_8()
        
        # Slide 9
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_9()
        
        # Slide 10
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_10()
       
        # Slide 11
        self.wait(3)
        self.remove(*self.mobjects)
        self.slide_11()
        
        self.wait(5)
    
    # slide pattern used in all slides
    def slide_pattern(self):
        background = Rectangle(
            width=config.frame_width,
            height=config.frame_height,
            color=BLACK,
            fill_opacity=1
        )
        self.add(background)
        decorative_image = ImageMobject("decorative_image.png") 
        decorative_image.scale(1.5) 
        decorative_image.move_to(UP * 3 + LEFT * 6)  
        self.add(decorative_image)
    
    # initial slide and so on after this
    def title_slide(self):
        background = ImageMobject("background_image.png") 
        background.scale_to_fit_width(config.frame_width)
        background.scale_to_fit_height(config.frame_height)
        self.add(background)

        self.wait(5)
        
        # Add the title
        if lang=='eng':
            title = Text("Simplified derivation \n of Schrödinger's equations", font_size=36, line_spacing=1)
        else:
            title = Text("Dedução simplificada\n das equações de Schrödinger", font_size=36, line_spacing=1)
        title.to_edge(DOWN)  
        title.shift(UP * 0.5 + LEFT * 1.2) 
        self.play(Write(title))
        self.wait(2)

    def slide_2(self):
       
        self.slide_pattern()

        if lang=='eng':
            title = Text("Schrödinger's equations", font_size=48)
        else:
            title = Text("Equações de Schrödinger", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait(1)

        schrodinger_image = ImageMobject("schrodinger_image.png")  
        schrodinger_image.move_to(UP * 1 + LEFT * 3)  
        self.play(FadeIn(schrodinger_image))

        grave_image = ImageMobject("grave_image.png")  
        grave_image.move_to(DOWN * 2 + LEFT * 3)  
        
        equation_time_dependent = MathTex(r"i \hbar \dot{\psi} = H \psi")
        equation_time_dependent.move_to(UP * 2 + RIGHT * 2)  
        equation_time_dependent.scale(0.2) 
        equation_time_dependent.move_to(grave_image.get_center() + UP * 0.4)  

        self.play(FadeIn(grave_image))
        self.wait(1)
        self.play(Write(equation_time_dependent))
        self.wait(1)
        self.play(
            equation_time_dependent.animate.move_to(UP + RIGHT * 2).scale(5),
            run_time=2
        )
        self.wait(1)
        
        equation_time_independent = MathTex(r"H \psi = E \psi")
        equation_time_independent.move_to(DOWN + RIGHT * 2)

        equation_copy = equation_time_dependent.copy()
        self.play(
            equation_copy.animate.move_to(equation_time_independent.get_center()),
            run_time=2
        )
        self.wait(1)

        self.play(Transform(equation_copy, equation_time_independent))
        self.wait(1)

        gif_image = ImageMobject("smiley_gif.png")
        gif_image.move_to(DOWN * 6)
        
        self.play(gif_image.animate.move_to(equation_time_dependent.get_center() + RIGHT*3 + DOWN))

        question_mark = Text("?", color=YELLOW_E)
        question_mark.next_to(gif_image, UP, buff=0.1)
        question_mark.shift(LEFT * 0.1)
        self.play(FadeIn(question_mark))

    def slide_3(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("The proton-electron system", font_size=48)
        else:
            title = Text("O sistema próton-elétron", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait(1)

        if lang=='eng':
            initial_text = ("Let's start by assuming that the proton and electron are \n"
                            "two point electric charges with invariant masses.")
        else:
            initial_text = ("Começamos admitindo que próton e elétron são duas \n"
                            "cargas elétricas pontuais, de massas invariantes.")
        initial_textbox = Text(initial_text, font_size=24, color=WHITE, line_spacing=1.5)
        initial_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(initial_textbox))

        self.wait(3)

        proton = Circle(color=RED, radius=0.4, fill_opacity=1)
        proton.move_to(LEFT * 3 + DOWN)  
        electron = Circle(color=BLUE, radius=0.2, fill_opacity=1)
        electron.move_to(RIGHT * 3 + DOWN)  

        if lang=='eng':
            proton_label_ini = Text("proton", font_size=24, color=WHITE)
            electron_label_ini = Text("electron", font_size=24, color=WHITE)
        else:
            proton_label_ini = Text("próton", font_size=24, color=WHITE)
            electron_label_ini = Text("elétron", font_size=24, color=WHITE)
        proton_label_ini.next_to(proton, LEFT)
        electron_label_ini.next_to(electron, RIGHT)

        self.play(FadeIn(proton), FadeIn(electron))
        self.play(Write(proton_label_ini), Write(electron_label_ini))

        self.wait(2)

        if lang=='eng':
            second_text = ("We place the proton fixed at the origin of the x-axis (x=0) \n"
                            "and the electron at an arbitrary position, x.")
        else:
            second_text = ("Colocamos o próton fixo na origem do eixo x (x=0) \n"
                            "e o elétron numa posição qualquer, x.")
        second_textbox = Text(second_text, font_size=24, color=WHITE, line_spacing=1.5)
        second_textbox.next_to(initial_textbox, DOWN, buff=0.5)
        self.play(Transform(initial_textbox, second_textbox))

        self.wait(5)

        # x-axis
        axis = NumberLine(
            x_range=(0, 7, 1),
            color=WHITE,
            include_numbers=False,
            include_tip=True,
            decimal_number_config={"num_decimal_places": 1}
        )
        axis.move_to(DOWN * 2)

        # proton and electron
        proton_label = Text("0", color=WHITE, font_size=24)
        proton_label.next_to(axis.n2p(0), DOWN, buff=0.5)
        electron_position = 5  # Posição genérica do elétron
        electron_label = Text("x", color=WHITE, font_size=24)
        electron_label.next_to(axis.n2p(electron_position), DOWN, buff=0.4)

        # new proton and electron
        new_proton = Circle(color=RED, radius=0.4, fill_opacity=1)
        new_proton.move_to(axis.n2p(0))  # Posição do próton na origem
        new_electron = Circle(color=BLUE, radius=0.2, fill_opacity=1)
        new_electron.move_to(axis.n2p(electron_position))  # Posição do elétron em x

        self.play(Create(axis))
        self.play(Transform(proton_label_ini, proton_label), Transform(electron_label_ini, electron_label))
        self.play(Transform(proton, new_proton), Transform(electron, new_electron))

        self.wait(1)
       
        if lang=="eng":
            third_textbox = Tex(
                r"\begin{flushleft}"
                r"The total energy, \(E\), of the electron-proton system is the \\"
                r"sum of the kinetic energy of the electron, \(E_k\), and \\"
                r"its potential energy, \(E_p\), relative to the proton."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
            third_textbox = Tex(
                r"\begin{flushleft}"
                r"A energia total, \(E\), do sistema elétron mais próton é \\"
                r"a soma da energia cinética do elétron, \(E_c\), com sua \\"
                r"energia potencial, \(E_p\), em relação ao próton."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        third_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(FadeOut(initial_textbox))
        self.play(Write(third_textbox))

        self.wait(7)

        # vector of v or p
        vector_v = Arrow(
            start=axis.n2p(electron_position),
            end=axis.n2p(3.2),
            color=GREEN_D,
            buff=0,
            stroke_width=6
        )
        label_v = MathTex("\\vec{v}")
        label_v.next_to(vector_v, UP, buff=0.1)

        self.play(Create(vector_v), Write(label_v))

        if lang=='eng':
            cin = 'k'
        else:
            cin = 'c'
        eqbox = MathTex(r"E=E_{{{}}}+E_p".format(cin))
        eqbox.next_to(third_textbox, DOWN, buff=0.5)
        self.play(Write(eqbox))

    def slide_4(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("Energies", font_size=48)
        else:
            title = Text("Energias", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        # x-axis
        axis = NumberLine(
            x_range=(0, 7, 1),
            color=WHITE,
            include_numbers=False,
            include_tip=True,
            decimal_number_config={"num_decimal_places": 1}
        )
        axis.move_to(DOWN * 2)

        # proton and electron
        proton_label = Text("0", color=WHITE, font_size=24)
        proton_label.next_to(axis.n2p(0), DOWN, buff=0.5)
        electron_position = 5  # Posição genérica do elétron
        electron_label = Text("x", color=WHITE, font_size=24)
        electron_label.next_to(axis.n2p(electron_position), DOWN, buff=0.4)

        # new proton and electron
        new_proton = Circle(color=RED, radius=0.4, fill_opacity=1)
        new_proton.move_to(axis.n2p(0))  # Posição do próton na origem
        new_electron = Circle(color=BLUE, radius=0.2, fill_opacity=1)
        new_electron.move_to(axis.n2p(electron_position))  # Posição do elétron em x

        # vector of v or p
        vector_v = Arrow(
            start=axis.n2p(electron_position),
            end=axis.n2p(3.2),
            color=GREEN_D,
            buff=0,
            stroke_width=6
        )
        label_v = MathTex("\\vec{v}")
        label_v.next_to(vector_v, UP, buff=0.1)

        self.play(Create(axis))
        self.play(FadeIn(proton_label), FadeIn(electron_label))
        self.play(FadeIn(new_proton), FadeIn(new_electron))
        self.play(Create(vector_v), Write(label_v))

        if lang=='eng':
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"The kinetic energy of the electron, \(E_k\), can be easily \\"
                r"calculated using the well-known relationship with \\"
                r"its mass, \(m_e\), and the magnitude of its velocity, \(v\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"A energia cinética do elétron, \(E_c\),pode ser facilmente  \\"
                r"calculada pela conhecida relação com sua massa,  \(m_e\), \\"
                r"e o módulo de sua velocidade, \(v\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        first_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(first_textbox))

        self.wait(7)

        if lang=='eng':
            cin = 'k'
        else:
            cin = 'c'
        eqbox1 = MathTex("E_{{{}}}".format(cin),"=","\\frac{m_ev^2}{2}")
        eqbox1.next_to(first_textbox, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        self.wait(2)

        if lang=='eng':
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"The momentum, \(p\), is given by, \\"
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"A quantidade de movimento, \(p\), é dada por, \\"
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        second_textbox.next_to(separation_line, DOWN, buff=1)
        self.play(FadeOut(first_textbox))
        self.play(Write(second_textbox))

        eqbox2 = MathTex("p=m_ev")
        eqbox2.next_to(second_textbox, RIGHT)
        self.play(Write(eqbox2))

        self.wait(2)

        eqbox3 = MathTex("E_{{{}}}".format(cin),"=","\\frac{m_ev^2}{2}","\\frac{m_e}{m_e}")
        eqbox3[3].set_color(YELLOW)
        eqbox3.move_to(eqbox1, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox1, eqbox3))

        self.wait(3)

        eqbox4 = MathTex("E_{{{}}}".format(cin),"=","\\frac{m_e^2v^2}{2m_e}")
        eqbox4.move_to(eqbox3, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox3, eqbox4))

        self.wait(3)

        eqbox5 = MathTex("E_{{{}}}".format(cin),"=","\\frac{(m_ev)^2}{2m_e}")
        eqbox5[2][1:4].set_color(YELLOW)
        eqbox5.move_to(eqbox4, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox4, eqbox5))

        self.wait(3)

        label2_v = MathTex("\\vec{p}")
        label2_v.next_to(vector_v, UP, buff=0.1)

        eqbox6 = MathTex("E_{{{}}}".format(cin),"=","\\frac{p^2}{2m_e}")
        eqbox6.move_to(eqbox5, aligned_edge=LEFT)
        self.play(FadeOut(second_textbox))
        self.play(
            eqbox2.animate.move_to(eqbox5[2], UP).scale(0),
            TransformMatchingTex(eqbox5, eqbox6),
            Transform(label_v, label2_v),
            run_time=3
        )
        self.play(FadeOut(eqbox2))
        self.wait(2)
        self.play(
            eqbox6.animate.move_to(LEFT * 5.8 + DOWN),
            run_time=2
        )

        if lang=='eng':
            third_textbox = Tex(
                r"\begin{flushleft}"
                r"The potential energy, \(E_p\), between two point charges \\"
                r"can be calculated using the well-known relationship \\"
                r"involving the vacuum permittivity, \(\epsilon_o\), the charges' \\"
                r"values, \(Q\) and \(q\), and the distance, \(d\), between them."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            third_textbox = Tex(
                r"\begin{flushleft}"
                r"A energia potencial, \(E_p\), entre duas cargas pontuais \\"
                r"pode ser calculada pela conhecida relação com a \\"
                r"permissividade elétrica do vácuo, \(\epsilon_o\), os valores \\"
                r"das cargas, \(Q\) e \(q\), e a distância, \(d\), entre elas."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        third_textbox.next_to(separation_line, DOWN, buff=0.3)
        self.play(Write(third_textbox))

        self.wait(8)

        eqbox7 = MathTex("E_p","=","\\frac{1}{4\pi\epsilon_o}","\\frac{Qq}{d}")
        eqbox7.next_to(third_textbox, DOWN, buff=0.2)
        self.play(Write(eqbox7))

        self.wait(3)

        self.play(FadeOut(third_textbox))
    
        if lang=='eng':
            forth_textbox = Tex(
                r"\begin{flushleft}"
                r"The electron's charge is \(-q_e\), and therefore, \\"
                r"the proton's charge is \(+q_e\).\\"
                r"The distance between the charges is \(x\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            forth_textbox = Tex(
                r"\begin{flushleft}"
                r"A carga do elétron é \(-q_e\) e, portanto, \\"
                r"a carga do próton é \(+q_e\).\\"
                r"A distância entre as cargas é igual a \(x\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        forth_textbox.next_to(separation_line, DOWN, buff=0.3)
        self.play(Write(forth_textbox))

        self.wait(3)

        eqbox7b = MathTex(r"Q=+q_e \\"
                          r"q=-q_e \\"
                          r"d=x")
        eqbox7b.next_to(eqbox7, RIGHT, buff=0.5)
        self.play(Write(eqbox7b))

        self.wait(5)
       
        eqbox8 = MathTex("E_p","=","\\frac{1}{4\pi\epsilon_o}","\\frac{q_e(-q_e)}{x}")
        eqbox8.move_to(eqbox7, aligned_edge=LEFT)

        self.play(
                eqbox7[3][0:2].animate.set_color(YELLOW),
                eqbox7[3][3].animate.set_color(YELLOW)
                )
        self.play(
                eqbox7b.animate.move_to(eqbox7[3]).scale(0),
                TransformMatchingTex(eqbox7, eqbox8),
                run_time=3
                )
        self.play(FadeOut(eqbox7b))

        self.wait(3)

        eqbox9 = MathTex("E_p","=","-","\\frac{1}{4\pi\epsilon_o}","\\frac{q_e^2}{x}")
        eqbox9.move_to(eqbox8, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox8, eqbox9))

        self.play(FadeOut(forth_textbox))

        self.wait(3)

        if lang=='eng':
            fifth_textbox = Tex(
                r"\begin{flushleft}"
                r"Since \(E_p\) depends only on \(x\), we can simplify \\"
                r"by indicating the potential energy with a \\"
                r"function, \(V(x)\), or simply \(V\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            fifth_textbox = Tex(
                r"\begin{flushleft}"
                r"Como \(E_p\) só depende de \(x\) podemos simplificar \\"
                r"indicando a energia potencial com uma função, \\"
                r"\(V(x)\) ou, simplesmente, \(V\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        fifth_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(fifth_textbox))

        self.wait(6)
        
        eqbox10 = MathTex("E_p","=","-","\\frac{1}{4\pi\epsilon_o}","\\frac{q_e^2}{x}","=","V(x)","=","V")
        eqbox10.move_to(eqbox9, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox9, eqbox10))

        self.wait(3)
        
        eqbox11 = MathTex("E_p","=","V")
        eqbox11.move_to(eqbox10, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eqbox10, eqbox11))

        self.play(FadeOut(fifth_textbox))

        self.play(
            eqbox11.animate.move_to(RIGHT * 5.8 + DOWN),
            run_time=2
        )

        if lang=='eng':
            sixth_textbox = Text("Summing up the energies.", font_size=24)
        else:
            sixth_textbox = Text("Somando as energias.", font_size=24)
        sixth_textbox.next_to(separation_line, DOWN*3)
        self.play(Write(sixth_textbox))

        eqbox12 = MathTex("E","=","E_{{{}}}".format(cin),"+","E_p")
        eqbox12.next_to(sixth_textbox, DOWN*3)
        self.play(Write(eqbox12))

        self.wait(3)
        
        eqbox13 = MathTex("E","=","\\frac{p^2}{2m_e}","+","V")
        eqbox13.move_to(eqbox12, aligned_edge=LEFT)
        self.play(FadeOut(sixth_textbox))
        self.play(
                eqbox12[2].animate.set_color(YELLOW),
                eqbox12[4].animate.set_color(YELLOW),
                )
        self.play(
            eqbox6.animate.move_to(eqbox12[2]).scale(0),
            eqbox11.animate.move_to(eqbox12[4]).scale(0),
            TransformMatchingTex(eqbox12, eqbox13),
            run_time=3
            )
        self.play(FadeOut(eqbox6), FadeOut(eqbox11))

    def slide_5(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("The eletron as a wave", font_size=48)
        else:
            title = Text("O elétron como onda", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        # x-axis
        axis = NumberLine(
            x_range=(0, 7, 1),
            color=WHITE,
            include_numbers=False,
            include_tip=True,
            decimal_number_config={"num_decimal_places": 1}
        )
        axis.move_to(DOWN * 2)

        # proton and electron
        proton_label = Text("0", color=WHITE, font_size=24)
        proton_label.next_to(axis.n2p(0), DOWN, buff=0.5)
        electron_position = 5  # Posição genérica do elétron
        electron_label = Text("x", color=WHITE, font_size=24)
        electron_label.next_to(axis.n2p(electron_position), DOWN, buff=0.4)

        # new proton and electron
        new_proton = Circle(color=RED, radius=0.4, fill_opacity=1)
        new_proton.move_to(axis.n2p(0))  # Posição do próton na origem
        
        self.play(Create(axis))
        self.play(FadeIn(proton_label), FadeIn(electron_label))
        self.play(FadeIn(new_proton))
       
        # gaussian curve
        gaussian_curve = ParametricFunction(
            lambda t: np.array([
                t,
                0.5 * np.exp(-(t/0.5)**2),
                0
            ]), 
            t_range=np.array([-1, 1]),
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1
        )

        # gaussian curve on the x-axis
        gaussian_curve.next_to(axis.number_to_point(5), UP*0.05)

        self.play(FadeIn(gaussian_curve))

        if lang=='eng':
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"The energy of an electromagnetic wave can be calculated \\"
                r"with the Planck-Einstein relation, which involves \\"
                r"Planck's constant, \(h\), and the wave's frequency, \(\nu\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"A energia de uma onda eletromagnética pode ser calculada \\"
                r"pela relação de Planck-Einstein, usando a constante \\"
                r"de Planck, \(h\), e a frequência da onda, \(\nu\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        first_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(first_textbox))

        self.wait(6)

        eqbox1 = MathTex("E","=","h","\\nu")
        eqbox1.next_to(first_textbox, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        self.wait(3)

        if lang=='eng':
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"From circular motion, we know \\"
                r"that the frequency, \(\nu\), is related \\"
                r"to the angular velocity, \(\omega\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"Do movimento circular sabemos que\\"
                r"a frequência, \(\nu\), se relaciona \\"
                r"com a velocidade angular, \(\omega\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        second_textbox.move_to(LEFT*2+UP*1.5)
        self.play(Transform(first_textbox, second_textbox))

        eqbox2 = MathTex("\\nu","=","\\frac{\\omega}{2\\pi}")
        eqbox2.next_to(first_textbox, RIGHT, buff=0.5)
        self.play(Write(eqbox2))

        self.wait(7)
        self.play(FadeOut(first_textbox))

        eqbox3 = MathTex("E","=","\\frac{h\\omega}{2\\pi}")
        eqbox3.move_to(eqbox1)
        self.play(eqbox1[3].animate.set_color(YELLOW))
        self.play(
            eqbox2.animate.move_to(eqbox1[3]).scale(0),
            TransformMatchingTex(eqbox1, eqbox3),
            run_time=3
        )
        self.play(FadeOut(eqbox2))

        self.wait(3)
        if lang=='eng':
            third_textbox = Tex(
                r"By convention,",
                font_size=40,
                color=WHITE,
                )
        else:
            third_textbox = Tex(
                r"Por convenção,",
                font_size=40,
                color=WHITE,
                )
        third_textbox.next_to(separation_line, DOWN, buff=1)
        self.play(Write(third_textbox))

        eqbox4 = MathTex("\\hbar","=","\\frac{h}{2\\pi}")
        eqbox4.next_to(third_textbox, RIGHT)
        self.play(Write(eqbox4))

        self.wait(4)

        eqbox5 = MathTex("E","=","\\hbar","\\omega")
        eqbox5.move_to(eqbox3)
        
        self.play(FadeOut(third_textbox))
        self.play(
                eqbox3[2][0].animate.set_color(YELLOW),
                eqbox3[2][2:].animate.set_color(YELLOW)
            )
        self.play(
            eqbox4.animate.move_to(eqbox3[2]).scale(0),
            TransformMatchingTex(eqbox3, eqbox5),
            run_time=3
            )
        self.play(FadeOut(eqbox4))

    def slide_6(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("Particle-wave duality", font_size=48)
        else:
            title = Text("A dualidade partícula-onda", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        # x-axis
        axis = NumberLine(
            x_range=(0, 7, 1),
            color=WHITE,
            include_numbers=False,
            include_tip=True,
            decimal_number_config={"num_decimal_places": 1}
        )
        axis.move_to(DOWN * 2)

        # proton and electron
        proton_label = Text("0", color=WHITE, font_size=24)
        proton_label.next_to(axis.n2p(0), DOWN, buff=0.5)
        electron_position = 5  # Posição genérica do elétron
        electron_label = Text("x", color=WHITE, font_size=24)
        electron_label.next_to(axis.n2p(electron_position), DOWN, buff=0.4)

        # new proton and electron
        new_proton = Circle(color=RED, radius=0.4, fill_opacity=1)
        new_proton.move_to(axis.n2p(0))  # Posição do próton na origem
        
        # vector v or p
        vector_v = Arrow(
            start=axis.n2p(electron_position),
            end=axis.n2p(3.2),
            color=GREEN_D,
            buff=0,
            stroke_width=6
        )
        
        self.play(Create(axis))
        self.play(FadeIn(proton_label), FadeIn(electron_label))
        self.play(FadeIn(new_proton))
       
        # gaussian curve
        gaussian_curve = ParametricFunction(
            lambda t: np.array([
                t,
                0.5 * np.exp(-(t/0.5)**2),
                0
            ]), 
            t_range=np.array([-1, 1]),
            color=BLUE,
            fill_color=BLUE,
            fill_opacity=1
        )

        # gaussian curve on x-axis
        gaussian_curve.next_to(axis.number_to_point(5), UP*0.05)

        self.play(FadeIn(gaussian_curve))

        # vector v into p
        label_v = MathTex("\\vec{p}")
        label_v.next_to(vector_v, UP, buff=0.1)
        self.play(Create(vector_v), Write(label_v))

        if lang=='eng':
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"Considering the particle-wave duality, we have the relationship \\"
                r"between the wavelength, \(\lambda\), and the linear momentum, \(p\), of \\"
                r"the particle according to the De Broglie equation."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            first_textbox = Tex(
                r"\begin{flushleft}"
                r"Considerando a dualidade partícula-onda, temos a relação \\"
                r"entre o comprimento de onda, \(\lambda\), e o momento linear, \(p\), \\"
                r"da partícula de acordo com a equação de De Broglie."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        first_textbox.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(first_textbox))

        self.wait(7)

        eqbox1 = MathTex("\\lambda","=","\\frac{h}{p}")
        eqbox1.next_to(first_textbox, DOWN)
        self.play(Write(eqbox1))

        self.wait(3)

        eqbox2 = MathTex("p","=","\\frac{h}{\\lambda}")
        eqbox2.move_to(eqbox1)
        self.play(TransformMatchingTex(eqbox1, eqbox2))

        self.wait(3)

        if lang=='eng':
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"The wavelength, \(\lambda\), relates \\"
                r"to the wave number, \(k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        else:
            second_textbox = Tex(
                r"\begin{flushleft}"
                r"O comprimento de onda, \(\lambda\), se \\"
                r"relaciona com o número de onda, \(k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
                )
        second_textbox.move_to(LEFT*2+UP*1.5)
        self.play(Transform(first_textbox, second_textbox))

        eqbox3 = MathTex("\\lambda","=","\\frac{2\\pi}{k}")
        eqbox3.next_to(second_textbox, RIGHT, buff=0.5)
        self.play(Write(eqbox3))

        self.wait(6)
        
        eqbox4 = MathTex("\\frac{1}{\\lambda}","=","\\frac{k}{2\\pi}")
        eqbox4.move_to(eqbox3)
        self.play(TransformMatchingTex(eqbox3, eqbox4))
        
        self.wait(3)
        self.play(FadeOut(first_textbox))

        eqbox5 = MathTex("p","=","\\frac{hk}{2\\pi}")
        eqbox5.move_to(eqbox2)
        self.play(eqbox2[2][1:].animate.set_color(YELLOW))
        self.play(
            eqbox4.animate.move_to(eqbox2[2]).scale(0),
            TransformMatchingTex(eqbox2, eqbox5),
            run_time=3
            )
        self.play(FadeOut(eqbox4))

        if lang=='eng':
            third_textbox = Tex(
                r"By convention,",
                font_size=40,
                color=WHITE,
                )
        else:
            third_textbox = Tex(
                r"Por convenção,",
                font_size=40,
                color=WHITE,
                )
        third_textbox.next_to(separation_line, DOWN, buff=1)
        self.play(Write(third_textbox))

        eqbox6 = MathTex("\\hbar","=","\\frac{h}{2\\pi}")
        eqbox6.next_to(third_textbox, RIGHT)
        self.play(Write(eqbox6))

        self.wait(3)

        eqbox7 = MathTex("p","=","{\\hbar}","k")
        eqbox7.move_to(eqbox5)
        
        self.play(FadeOut(third_textbox))
        self.play(
            eqbox5[2][0].animate.set_color(YELLOW),
            eqbox5[2][2:].animate.set_color(YELLOW)
            )
        self.play(
            eqbox6.animate.move_to(eqbox5[2]).scale(0),
            TransformMatchingTex(eqbox5, eqbox7),
            run_time=3
            )
        self.play(FadeOut(eqbox6))

    def slide_7(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("The energy equation", font_size=48)
        else:
            title = Text("A equação de energia", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))
        
        eqbox1 = MathTex("E","=","\\frac{p^2}{2m_e}","+","V")
        self.play(Write(eqbox1))

        self.wait(4)

        eqbox2 = MathTex("E","=","\\hbar","\\omega")
        eqbox2.move_to(LEFT*4+DOWN*1.5)
        self.play(Write(eqbox2))

        if lang=='eng':
            textbox1 = Text('Eletcron as a wave', font_size=20)
        else:
            textbox1 = Text('Elétron como onda', font_size=20)
        textbox1.next_to(eqbox2, UP)
        self.play(Write(textbox1))

        self.wait(4)

        eqbox3 = MathTex("p","=","{\\hbar}","k")
        eqbox3.move_to(RIGHT*4+DOWN*1.5)
        self.play(Write(eqbox3))

        if lang=='eng':
            textbox2 = Text('Particle-wave duality', font_size=20)
        else:
            textbox2 = Text('Dualidade partícula-onda', font_size=20)
        textbox2.next_to(eqbox3, UP)
        self.play(Write(textbox2))

        eqbox4 = MathTex("\\hbar","\\omega","=","\\frac{p^2}{2m_e}","+","V")
        eqbox4.move_to(eqbox1)
        
        self.play(FadeOut(textbox1))
        self.play(eqbox1[0].animate.set_color(YELLOW))
        self.play(
            eqbox2.animate.move_to(eqbox1[0]).scale(0),
            TransformMatchingTex(eqbox1, eqbox4),
            run_time=3
        )
        self.play(FadeOut(eqbox2))

        eqbox5 = MathTex("\\hbar","\\omega","=","\\frac{({\hbar}k)^2}{2m_e}","+","V")
        eqbox5.move_to(eqbox4)

        self.play(FadeOut(textbox2))
        self.play(eqbox4[3][0].animate.set_color(YELLOW))
        self.play(
            eqbox3.animate.move_to(eqbox4[3]).scale(0),
            TransformMatchingTex(eqbox4, eqbox5),
            run_time=3
            )
        self.play(FadeOut(eqbox3))

        self.wait(3)

        eqbox6 = MathTex("\\hbar","\\omega","=","\\frac{\hbar^2k^2}{2m_e}","+","V")
        eqbox6.move_to(eqbox5)
        self.play(TransformMatchingTex(eqbox5, eqbox6))

    def slide_8(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("The wave function", font_size=48)
        else:
            title = Text("A função de Onda", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        if lang=='eng':
            textbox1 = Text('Complex wave function in exponential form.', font_size=24)
        else:
            textbox1 = Text('Função de onda complexa na forma exponencial.', font_size=24)
        textbox1.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(textbox1))

        eqbox1 = MathTex("\\psi","=","C","e^{i(kx-{\\omega}t)}")
        eqbox1.next_to(textbox1, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        if lang=='eng':
            textbox1b = Tex(r"\begin{flushleft}"
                            r"\(\psi\): wave function with position, \(x\), and time, \(t\) \\"
                            r"\(C\): constant that combines the amplitude and phase of the wave \\"
                            r"\(i\): imaginary number \(\sqrt{-1}\) \\"
                            r"\(k\): wave number \\"
                            r"\(\omega\): angular speed or frequency"
                            r"\end{flushleft}",
                            font_size=32)
        else:
            textbox1b = Tex(r"\begin{flushleft}"
                            r"\(\psi\): função de onda com a posição, \(x\), e o tempo, \(t\) \\"
                            r"\(C\): constante que reune a amplitude e a fase da onda \\"
                            r"\(i\): número imaginário \(\sqrt{-1}\) \\"
                            r"\(k\): número de onda \\"
                            r"\(\omega\): velocidade ou frequência angular"
                            r"\end{flushleft}",
                            font_size=32)
        textbox1b.next_to(eqbox1, DOWN, buff=0.3)
        self.play(Write(textbox1b))
                
        self.wait(10)
        self.play(FadeOut(textbox1b))

        if lang=='eng':
            textbox2 = Text("The first derivative \n"
                        "with respect to time.", 
                        font_size=22)
        else:
            textbox2 = Text("A primeira derivada \n"
                        "em relação ao tempo.", 
                        font_size=22)
        textbox2.move_to(LEFT*3)
        self.play(Write(textbox2))

        eqbox2 = MathTex("\\frac{\\partial \\psi}{\\partial t}","=","C","e^{i(kx-{\\omega}t)}","(-i\\omega)")
        eqbox2.next_to(textbox2, DOWN, buff=0.5)
        self.play(Write(eqbox2))

        self.wait(3)

        eqbox3 = MathTex("\\frac{\\partial \\psi}{\\partial t}","=","\\psi","(-i\\omega)")
        eqbox3.move_to(eqbox2)

        self.play(eqbox2[2:4].animate.set_color(YELLOW))
        self.play(
                eqbox1.copy().animate.move_to(eqbox2[3]).scale(0),
                TransformMatchingTex(eqbox2, eqbox3),
                run_time=3
                )
        
        self.wait(3)

        eqbox4 = MathTex("\\frac{\\partial \\psi}{\\partial t}","=","-i","\\omega","\\psi")
        eqbox4.move_to(eqbox3)
        self.play(TransformMatchingTex(eqbox3, eqbox4))

        self.wait(3)

        eqbox5 = MathTex("-i","\\omega","\\psi","=","\\frac{\\partial \\psi}{\\partial t}")
        eqbox5.move_to(eqbox4)
        self.play(TransformMatchingTex(eqbox4, eqbox5))

        self.wait(3)

        eqbox6 = MathTex("\\omega","=","-","\\frac{1}{i\\psi}","\\frac{\\partial \\psi}{\\partial t}")
        eqbox6.move_to(eqbox5)
        self.play(TransformMatchingTex(eqbox5, eqbox6))

        self.wait(3)

        self.play(FadeOut(textbox2))

        if lang=='eng':
            textbox3 = Text("The first derivative \n"
                        "with respect to x.", 
                        font_size=22)
        else:
            textbox3 = Text("A primeira derivada \n"
                        "em relação a x.", 
                        font_size=22)
        textbox3.move_to(RIGHT*3)
        self.play(Write(textbox3))

        eqbox7 = MathTex("\\frac{\\partial \\psi}{\\partial x}","=","C","e^{i(kx-{\\omega}t)}","i","k")
        eqbox7.next_to(textbox3, DOWN, buff=0.5)
        self.play(Write(eqbox7))

        self.wait(3)

        if lang=='eng':
            textbox3b = Text("The second derivative \n"
                        "with respect to x.", 
                        font_size=22)
        else:
            textbox3b = Text("A segunda derivada \n"
                        "em relação a x.", 
                        font_size=22)
        textbox3b.move_to(textbox3)
        self.play(Transform(textbox3, textbox3b))

        eqbox8 = MathTex("\\frac{\\partial^2 \\psi}{\\partial x^2}","=","C","e^{i(kx-{\\omega}t)}","i","k","i","k")
        eqbox8.move_to(eqbox7)
        self.play(TransformMatchingTex(eqbox7, eqbox8))

        self.wait(3)

        eqbox9 = MathTex("\\frac{\\partial^2 \\psi}{\\partial x^2}","=","C","e^{i(kx-{\\omega}t)}","i^2","k^2")
        eqbox9.move_to(eqbox8)
        self.play(TransformMatchingTex(eqbox8, eqbox9))

        self.wait(3)

        eqbox10 = MathTex("\\frac{\\partial^2 \\psi}{\\partial x^2}","=","C","e^{i(kx-{\\omega}t)}","(-k^2)")
        eqbox10.move_to(eqbox9)
        self.play(TransformMatchingTex(eqbox9, eqbox10))

        self.wait(3)

        eqbox11 = MathTex("\\frac{\\partial^2 \\psi}{\\partial x^2}","=","\\psi","(-k^2)")
        eqbox11.move_to(eqbox10)

        self.play(eqbox10[2:4].animate.set_color(YELLOW))
        self.play(
                eqbox1.copy().animate.move_to(eqbox10[3]).scale(0),
                TransformMatchingTex(eqbox10, eqbox11),
                run_time=3
                )

        self.wait(3)

        eqbox12 = MathTex("\\frac{\\partial^2 \\psi}{\\partial x^2}","=","-","k^2","\\psi")
        eqbox12.move_to(eqbox11)
        self.play(TransformMatchingTex(eqbox11, eqbox12))

        self.wait(3)

        eqbox13 = MathTex("-","k^2","\\psi","=","\\frac{\\partial^2 \\psi}{\\partial x^2}")
        eqbox13.move_to(eqbox12)
        self.play(TransformMatchingTex(eqbox12, eqbox13))

        self.wait(3)

        eqbox14 = MathTex("k^2","=","-","\\frac{1}{\psi}","\\frac{\\partial^2 \\psi}{\\partial x^2}")
        eqbox14.move_to(eqbox13)
        self.play(TransformMatchingTex(eqbox13, eqbox14))

        self.play(FadeOut(textbox3))

    def slide_9(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("Variable energy", font_size=48)
        else:
            title = Text("Energia variável", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))
 
        if lang=='eng':
            textbox1 = Text('Energy equation', font_size=24)
        else:
            textbox1 = Text('Equação de energia', font_size=24)
        textbox1.next_to(separation_line, DOWN, buff=1)
        self.play(Write(textbox1))

        eqbox1 = MathTex("\\hbar","\\omega","=","\\frac{\hbar^2k^2}{2m_e}","+","V")
        eqbox1.next_to(textbox1, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        self.wait(4)

        self.play(FadeOut(textbox1))

        eqbox2 = MathTex(r"\omega=-\frac{1}{i\psi}\frac{\partial\psi}{\partial t}")
        eqbox2.move_to(LEFT*4 + DOWN*1.5)
        self.play(Write(eqbox2))

        self.wait(3)

        eqbox3 = MathTex(r"k^2=-\frac{1}{\psi}\frac{\partial^2\psi}{\partial x^2}")
        eqbox3.move_to(RIGHT*4 + DOWN*1.5)
        self.play(Write(eqbox3))

        self.wait(3)

        eqbox4 = MathTex("-","\\frac{\\hbar}{i\\psi}","\\frac{\\partial\\psi}{\\partial t}","=","\\frac{\\hbar^2k^2}{2m_e}","+","V")
        eqbox4.move_to(eqbox1)

        self.play(eqbox1[1].animate.set_color(YELLOW))
        self.play(
            eqbox2.animate.move_to(eqbox1[1]).scale(0),
            TransformMatchingTex(eqbox1, eqbox4),
            run_time=3
        )
        self.play(FadeOut(eqbox2))

        self.wait(3)

        eqbox5 = MathTex("-","\\frac{\\hbar}{i\\psi}","\\frac{\\partial\\psi}{\\partial t}","=","-","\\frac{\\hbar^2}{2m_e\\psi}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V")
        eqbox5.move_to(eqbox4)

        self.play(eqbox4[4][2:4].animate.set_color(YELLOW))
        self.play(
            eqbox3.animate.move_to(eqbox4[4], UP).scale(0),
            TransformMatchingTex(eqbox4, eqbox5),
            run_time=3
        )
        self.play(FadeOut(eqbox3))

        self.wait(3)

        eqbox6 = MathTex("-","\\frac{\\hbar}{i\\psi}","\\frac{\\partial\\psi}{\\partial t}","\\psi","=","-","\\frac{\\hbar^2}{2m_e\\psi}","\\frac{\\partial^2\\psi}{\\partial x^2}","\\psi","+","V\\psi")
        eqbox6[3].set_color(YELLOW)
        eqbox6[8].set_color(YELLOW)
        eqbox6[10][1].set_color(YELLOW)
        eqbox6.move_to(eqbox5)
        self.play(TransformMatchingTex(eqbox5, eqbox6))

        self.wait(3)

        self.play(
            eqbox6[1][3].animate.set_color(YELLOW),
            eqbox6[6][6].animate.set_color(YELLOW)
            )
        
        self.wait(3)

        self.play(
                eqbox6[1][3].animate.scale(0),
                eqbox6[3].animate.scale(0),
                eqbox6[6][6].animate.scale(0),
                eqbox6[8].animate.scale(0),
                run_time=3
                )
    
        eqbox7 = MathTex("-","\\frac{\\hbar}{i}","\\frac{\\partial\\psi}{\\partial t}","=","-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V\\psi")
        eqbox7.move_to(eqbox6)
        self.play(TransformMatchingTex(eqbox6, eqbox7))

        self.wait(3)

        self.play(eqbox7[0].animate.set_color(YELLOW))

        eqbox8 = MathTex("i^2","\\frac{\\hbar}{i}","\\frac{\\partial\\psi}{\\partial t}","=","-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V\\psi")
        eqbox8[0].set_color(YELLOW)
        eqbox8.move_to(eqbox7)
        self.play(TransformMatchingTex(eqbox7, eqbox8))

        self.wait(3)

        self.play(eqbox8[1][2].animate.set_color(YELLOW))
        self.play(
                eqbox8[0][1].animate.scale(0),
                eqbox8[1][1].animate.scale(0),
                eqbox8[1][2].animate.scale(0),
                run_time=3
                )

        eqbox9 = MathTex("i","\\hbar","\\frac{\\partial\\psi}{\\partial t}","=","-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V\\psi")
        eqbox9.move_to(eqbox8)
        self.play(TransformMatchingTex(eqbox8, eqbox9))

        self.wait(3)

        if lang=='eng':
            textbox2 = Text("Time-dependent Schrödinger's equation.", font_size=24)
        else:
            textbox2 = Text('Equação de Schrödinger dependente do tempo.', font_size=24)
        textbox2.next_to(eqbox1, UP, buff=0.5)
        self.play(Write(textbox2))

    def slide_10(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("Constant energy", font_size=48)
        else:
            title = Text("Energia constante", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        if lang=='eng':
            textbox1 = Text('Energy equation for a constant energy.', font_size=24)
        else:
            textbox1 = Text('Equação de energia para uma energia constante.', font_size=24)
        textbox1.next_to(separation_line, DOWN, buff=1)
        self.play(Write(textbox1))

        if lang=='eng':
            eqbox1 = MathTex("E","=","\\frac{p^2}{2m_e}","+","V","=","\\underline{const}")
        else:
            eqbox1 = MathTex("E","=","\\frac{p^2}{2m_e}","+","V","=","\\underline{cte}")
        eqbox1.next_to(textbox1, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        self.wait(4)

        self.play(FadeOut(textbox1))

        eqbox2 = MathTex("\\frac{p^2}{2m_e}","+","V","=","E")
        eqbox2.move_to(eqbox1)
        self.play(TransformMatchingTex(eqbox1, eqbox2))

        self.wait(3)

        eqbox3 = MathTex(r"p=\hbar{k}")
        eqbox3.next_to(LEFT + DOWN)
        self.play(Write(eqbox3))

        self.wait(3)

        eqbox4 = MathTex("\\frac{(\\hbar{k})^2}{2m_e}","+","V","=","E")
        eqbox4.move_to(eqbox2)
        
        self.play(eqbox2[0][0].animate.set_color(YELLOW))
        self.play(
            eqbox3.animate.move_to(eqbox2[0], UP).scale(0),
            TransformMatchingTex(eqbox2, eqbox4),
            run_time=3
        )
        self.play(FadeOut(eqbox3))

        self.wait(3)

        eqbox5 = MathTex("\\frac{\\hbar^2k^2}{2m_e}","+","V","=","E")
        eqbox5.move_to(eqbox4)
        self.play(TransformMatchingTex(eqbox4, eqbox5))

        self.wait(3)

        eqbox6 = MathTex(r"k^2=-\frac{1}{\psi}\frac{\partial^2\psi}{\partial x^2}")
        eqbox6.next_to(eqbox5, LEFT + DOWN)
        self.play(Write(eqbox6))

        self.wait(3)

        eqbox7 = MathTex("-","\\frac{\\hbar^2}{2m_e\\psi}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V","=","E")
        eqbox7.move_to(eqbox5)

        self.play(eqbox5[0][2:4].animate.set_color(YELLOW))
        self.play(
            eqbox6.animate.move_to(eqbox5[0], UP).scale(0),
            TransformMatchingTex(eqbox5, eqbox7),
            run_time=3
        )
        self.play(FadeOut(eqbox6))

        self.wait(3)     

        eqbox8 = MathTex("-","\\frac{\\hbar^2}{2m_e\\psi}","\\frac{\\partial^2\\psi}{\\partial x^2}","\\psi","+","V\\psi","=","E\\psi")
        eqbox8[3].set_color(YELLOW)
        eqbox8[5][1].set_color(YELLOW)
        eqbox8[7][1].set_color(YELLOW)
        eqbox8.move_to(eqbox7)
        self.play(TransformMatchingTex(eqbox7, eqbox8))

        self.wait(3)

        self.play(eqbox8[1][6].animate.set_color(YELLOW))
        self.play(
                eqbox8[1][6].animate.scale(0),
                eqbox8[3].animate.scale(0),
                run_time=3
                )

        eqbox9 = MathTex("-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V\\psi","=","E\\psi")
        eqbox9.move_to(eqbox8)
        self.play(TransformMatchingTex(eqbox8, eqbox9))

        self.wait(3)

        if lang=='eng':
            textbox2 = Text("Time-independent Schrödinger's equation.", font_size=24)
        else:
            textbox2 = Text('Equação de Schrödinger independente do tempo.', font_size=24)
        textbox2.next_to(eqbox1, UP, buff=0.5)
        self.play(Write(textbox2))

    def slide_11(self):
        self.slide_pattern()

        if lang=='eng':
            title = Text("Schrödinger's equations", font_size=48)
        else:
            title = Text("Equações de Schrödinger", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        if lang=='eng':
            textbox1 = Text('Time-dependent', font_size=24)
        else:
            textbox1 = Text('Dependente do tempo', font_size=24)
        textbox1.next_to(separation_line, DOWN, buff=0.5)
        self.play(Write(textbox1))

        eqbox1 = MathTex("i","\\hbar","\\frac{\\partial\\psi}{\\partial t}","=","-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V","\\psi")
        eqbox1.next_to(textbox1, DOWN, buff=0.5)
        self.play(Write(eqbox1))

        if lang=='eng':
            textbox2 = Text('Time-independent', font_size=24)
        else:
            textbox2 = Text('Independente do tempo', font_size=24)
        textbox2.next_to(eqbox1, DOWN, buff=1)
        self.play(Write(textbox2))

        eqbox2 = MathTex("-","\\frac{\\hbar^2}{2m_e}","\\frac{\\partial^2\\psi}{\\partial x^2}","+","V","\\psi","=","E","\\psi")
        eqbox2.next_to(textbox2, DOWN, buff=0.5)
        self.play(Write(eqbox2))

        self.wait(3)

        eqbox3 =  MathTex(r"H=-\frac{\hbar^2}{2m_e}\frac{\partial^2}{\partial x^2}+V", font_size=32)
        eqbox3.move_to(LEFT*5)
        self.play(Write(eqbox3))

        if lang=='eng':
            textbox3 = Text('Hamiltonian operator', font_size=18)
        else:
            textbox3 = Text('Operador Hamiltoniano', font_size=18)
        textbox3.next_to(eqbox3, UP, buff=0.1)
        self.play(Write(textbox3))

        self.wait(4)

        eqbox4 = MathTex("i","\\hbar","\\frac{\\partial\\psi}{\\partial t}","=","\\left(-\\frac{\\hbar^2}{2m_e}\\frac{\\partial^2}{\\partial x^2}+V\\right)","\\psi")
        eqbox4.move_to(eqbox1)
        self.play(TransformMatchingTex(eqbox1, eqbox4))

        self.wait(3)

        eqbox5 = MathTex("\\left(-\\frac{\\hbar^2}{2m_e}\\frac{\\partial^2}{\\partial x^2}+V\\right)","\\psi","=","E","\\psi")
        eqbox5.move_to(eqbox2)
        self.play(TransformMatchingTex(eqbox2, eqbox5))

        self.wait(3)

        self.play(FadeOut(textbox3))

        eqbox6 = MathTex("i","\\hbar","\\frac{\\partial\\psi}{\\partial t}","=","H","\\psi")
        eqbox6.move_to(eqbox4)
       
        eqbox3copy = eqbox3.copy()
        self.play(eqbox4[4].animate.set_color(YELLOW))
        self.play(
            eqbox3copy.animate.move_to(eqbox4[4]).scale(0),
            TransformMatchingTex(eqbox4, eqbox6),
            run_time=3
        )
        self.play(FadeOut(eqbox3copy))

        self.wait(3)

        eqbox7 = MathTex("H","\\psi","=","E","\\psi")
        eqbox7.move_to(eqbox5)
        
        self.play(eqbox5[0].animate.set_color(YELLOW))
        self.play(
            eqbox3.animate.move_to(eqbox5[0]).scale(0),
            TransformMatchingTex(eqbox5, eqbox7),
            run_time=3
        )
        self.play(FadeOut(eqbox3))

        eqbox8 = MathTex(r"\dot{\psi}=\frac{\partial\psi}{\partial t}")
        eqbox8.move_to(LEFT*5)

        if lang=='eng':
            textbox4 = Text('By convention', font_size=20)
        else:
            textbox4 = Text('Por convenção', font_size=20)
        textbox4.next_to(eqbox8, UP, buff=0.2)

        self.play(Write(textbox4))
        self.play(Write(eqbox8))

        self.wait(4)

        eqbox9 = MathTex("i","\\hbar","\\dot{\\psi}","=","H","\\psi")
        eqbox9.move_to(eqbox6)

        self.play(FadeOut(textbox4))

        self.play(eqbox6[2].animate.set_color(YELLOW))
        self.play(
            eqbox8.animate.move_to(eqbox6[2]).scale(0),
            TransformMatchingTex(eqbox6, eqbox9),
            run_time=3
        )
        self.play(FadeOut(eqbox8))

        self.wait(3)

        emoticon_fim = ImageMobject("pngegg.png")
        emoticon_fim.move_to(DOWN * 6)
        
        self.play(emoticon_fim.animate.move_to(RIGHT*5))

# Main        
if __name__ == "__main__":

    # configurations
    config.max_files_cached = 300 # cached files
    # language
    lang = 'eng'
    #lang='port' 

    # Render the scene directly from the script
    if lang=='eng':
        config.output_file = "Schrodinger_derivation.mp4"
    else:
        config.output_file = "Deducao_Schrodinger.mp4"
    scene = SchrodingerPresentation()
    scene.render()
