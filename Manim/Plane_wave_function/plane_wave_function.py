"""
Uniform plane wave function

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It produces a mp4 movie explaining the uniform plane wave
function in its complex form

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for undergrad students.

Packages needed:
manim
ps.: must have Latex in your system

Usage:
$ plane_wave_function.py

You can choose between english or portuguese (Brazil)
by setting the variable 'lang' in the #Main

Date: July/2024
Version: 1.0
"""

from manim import *

class plane_wave_function(ThreeDScene):
    def construct(self):

        
        self.cover()
        
        self.remove(*self.mobjects)
        self.slide_1()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_2()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_3()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_4()
        self.wait()
        
        self.remove(*self.mobjects)
        self.slide_5()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_6()
        self.wait(3)

        self.remove(*self.mobjects)
        self.slide_7()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_8()
        self.wait(5)
        
    # slide pattern used in all slides
    def slide_pattern(self):
        decorative_image = ImageMobject("wave.jpg") 
        decorative_image.scale(0.3) 
        decorative_image.to_edge(UP + LEFT)  
        self.add(decorative_image)

    # função para coseno animado
    def onda(self, A=1, k=1, w=1, d=0, t=0):
        
        x_min = -2.2*PI  # limite inferior do x
        x_max = 2.2*PI  # limite superior do x

        # Eixos para o gráfico da onda cosseno
        axes = Axes(
            x_range=[x_min, x_max, PI / 4],
            y_range=[-2.5, 2.5, 0.5],
            axis_config={"color": BLUE, 'tip_height':0.2, 'tip_width':0.1},
            y_axis_config={"include_numbers": True,
                           "numbers_to_include": list(range(-2,3,1)),
                           "decimal_number_config": {
                               "num_decimal_places": 0,
                            }
            }
        )

        # Definição dos rótulos personalizados
        x_labels = {
            -2*PI: MathTex("-2\\pi"),
            -3*PI/2: MathTex("-\\frac{3\\pi}{2}"),
            -PI: MathTex("-\\pi"),
            -PI/2: MathTex("-\\frac{\\pi}{2}"),
            PI/2: MathTex("\\frac{\\pi}{2}"),
            PI: MathTex("\\pi"),
            3*PI/2: MathTex("\\frac{3\\pi}{2}"),
            2*PI: MathTex("2\\pi"),
        }

        # Adiciona os rótulos aos eixos
        for x, label in x_labels.items():
            axes.get_x_axis().add_labels({x: label})

        cos_graph = axes.plot(lambda x: A*np.cos(k*x-w*t+d), color=YELLOW)

        #sin_graph = axes.plot(lambda x: A*np.sin(k*x-w*t+d), color=PURPLE)

        #return VGroup(axes, cos_graph, sin_graph)
        return VGroup(axes, cos_graph)
    
    def cover(self):

        tracker = ValueTracker(0)

        # Configurando os eixos 3D
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-4, 4, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        )

        axes.scale(0.7).rotate(axis=[0.65,0.38,0.65], angle=-83*DEGREES)

        # Função de onda cosseno
        def cos_wave(x, y, t=0):
            return np.cos(PI * (x + y - t))
                  
        # Superfície da onda cosseno
        surface1 = always_redraw(lambda: 
                    Surface(
                        lambda u, v: axes.c2p(u, v, cos_wave(u, v, tracker.get_value())+2),
                        u_range=[-3, 3],
                        v_range=[-3, 3],
                        resolution=(30, 30),
                        fill_opacity=0.8,
                        checkerboard_colors=[GREEN, RED]
                    )
                )
        # Superfície da onda cosseno
        surface2 = always_redraw(lambda: 
                    Surface(
                        lambda u, v: axes.c2p(u, v, cos_wave(u, v, tracker.get_value())),
                        u_range=[-3, 3],
                        v_range=[-3, 3],
                        resolution=(30, 30),
                        fill_opacity=0.8,
                        checkerboard_colors=[YELLOW, BLUE]
                    )
                )
        # Superfície da onda cosseno
        surface3 = always_redraw(lambda: 
                    Surface(
                        lambda u, v: axes.c2p(u, v, cos_wave(u, v, tracker.get_value())-2),
                        u_range=[-3, 3],
                        v_range=[-3, 3],
                        resolution=(30, 30),
                        fill_opacity=0.8,
                        checkerboard_colors=[PURPLE, PINK]
                    )
                )
        
        self.add(surface1, surface2, surface3)

        # Add the title
        if lang=='eng':
            title = Text("Uniform plane wave function", font_size=48)
        else:
            title = Text("Função de onda plana e uniforme", font_size=48)
        title.next_to(surface1, UP)
        
        
        # nimação do movimento da onda no tempo
        self.play(
            tracker.animate.set_value(8),
            run_time=4,
            rate_func=linear
        )
        # Animação do movimento da onda no tempo
        self.play(
            tracker.animate.set_value(4),
            Write(title),
            run_time=2,
            rate_func=linear
        )
        # Animação do movimento da onda no tempo
        self.play(
            tracker.animate.set_value(8),
            run_time=4,
            rate_func=linear
        )
 
    def slide_1(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The cosine function", font_size=48)
        else:
            title = Text("A função cosseno", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang=='eng':
            text_1 = ("The cosine function produces a static wave along an axis that \n"
                      "represents the angles, for example, the x-axis, when we take \n"
                      "the y-axis to represent the cosine values.")
        else:
            text_1 = ("A função cosseno produz uma onda estática ao longo de um eixo \n"
                      "que representa os ângulos, por exemplo, o eixo x, quando \n"
                      "tomamos o eixo y para representar os valores do cosseno.")
        textbox_1 = Text(text_1, font_size=24, color=WHITE, line_spacing=1.5)
        textbox_1.next_to(title, DOWN, buff=0.5)
        self.play(Write(textbox_1))

        self.wait(9)

        eq1 =  MathTex("y","=","f(x)","=","cos","(x)")
        eq1.next_to(textbox_1, DOWN*2, aligned_edge=LEFT)

        grafico = self.onda().scale(0.7).next_to(textbox_1, DOWN, aligned_edge=RIGHT)

        self.play(Create(grafico), Write(eq1), run_time=4)

        self.wait(2)

        line_graph1 = grafico[0].plot_line_graph(
            x_values = [-2*PI],
            y_values = [1],
            vertex_dot_style={"fill_color": GREEN},
        )

        line_graph2 = grafico[0].plot_line_graph(
            x_values = [-PI],
            y_values = [-1],
            vertex_dot_style={"fill_color": GREEN},
        )

        if lang == "eng":
            text_2 = ("Crest")
            text_3 = ("Trough")
        else:
            text_2 = ("Crista")
            text_3 = ("Vale")
        
        textbox_2 = Text(text_2, font_size=16).next_to(line_graph1, UP, buff=0.05)
        textbox_3 = Text(text_3, font_size=16).next_to(line_graph2, DOWN, buff=0.05)

        self.add(line_graph1, line_graph2)
        self.play(Write(textbox_2), Write(textbox_3))

        self.wait(3)

    def slide_2(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The wave number", font_size=48)
        else:
            title = Text("O número de onda", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Tex(
                r"\begin{flushleft}"
                r"In this plot, the wavelength, \(\lambda\), is \(2\pi\), meaning the wave \\"
                r"repeats at intervals of \(2\pi\) along \(x\). If we want to change \\"
                r"this wavelength, we need to multiply \(x\) by a constant, \(k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
             textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Neste gráfico o comprimento da onda, \(\lambda\), é de \(2\pi\), ou seja, a onda se \\"
                r"repete em intervalos de \(2\pi\) ao longo de \(x\). Se quisermos mudar esse \\"
                r"comprimento de onda precisamos multiplicar \(x\) por uma constante, \(k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        textbox_1.next_to(title, DOWN, buff=0.5)
                
        eq1 =  MathTex("f(x)","=","cos","(x)")
        eq1.next_to(textbox_1, DOWN*2, aligned_edge=LEFT)

        grafico1 = self.onda().scale(0.7).next_to(textbox_1, DOWN, aligned_edge=RIGHT)

        line_graph1 = grafico1[0].plot_line_graph(
            x_values = [0, 2*PI],
            y_values = [1, 1],
            vertex_dot_style={"fill_color": GREEN},
            line_color=RED,
            stroke_width = 2
        )

        textbox_2 = MathTex("\\lambda").scale(0.8).next_to(line_graph1, UP, buff=0.01)

        self.add(grafico1, eq1, line_graph1, textbox_2)
        self.play(Write(textbox_1))

        self.wait(9)
           
        eq2 = MathTex("f(x)","=","cos","(kx)")
        eq2.move_to(eq1, aligned_edge=LEFT)
        eq3 = MathTex("k","=","1")
        eq3.next_to(eq1, DOWN, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq1, eq2), Write(eq3))

        if lang == "eng":
            textbox_3 = Tex(
                r"\begin{flushleft}"
                r"If \(k=1\), then the wavelength is equal to \(2\pi\), as seen before. \\"
                r"If \(k=2\), then the cosine will reach the value of 1 (maximum) when \\"
                r"\(x=\pi\), meaning the wavelength, \(\lambda\), is reduced to half of the original."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
        else:
             textbox_3 = Tex(
                r"\begin{flushleft}"
                r"Se \(k=1\) então o comprimento de onda é igual a \(2\pi\), como visto antes. \\"
                r"Se \(k=2\) então o cosseno atingirá o valor de 1 (máximo) quando \(x=\pi\), \\"
                r" ou seja, o comprimento de onda, \(\lambda\), se reduz à metade do original."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
             
        self.play(Transform(textbox_1, textbox_3))

        self.wait(9)

        eq4 = MathTex("k","=","2")
        eq4.move_to(eq3, aligned_edge=LEFT)
        self.play(Transform(eq3, eq4))

        grafico2 = self.onda(k=2).scale(0.7).move_to(grafico1)

        line_graph2 = grafico2[0].plot_line_graph(
            x_values = [0, PI],
            y_values = [1,1],
            vertex_dot_style={"fill_color": GREEN},
            line_color=RED,
            stroke_width = 2
        )

        self.play(
                TransformMatchingShapes(grafico1, grafico2),
                TransformMatchingShapes(line_graph1, line_graph2),
                textbox_2.animate.next_to(line_graph2, UP, buff=0.01)
                )
        
        self.wait(3)
        
        self.play(
                Uncreate(grafico2),
                Uncreate(line_graph2),
                Unwrite(textbox_2),
                Unwrite(eq3),
                Unwrite(eq2),
                )
        
        if lang == "eng":
            textbox_4 = Tex(
                r"We conclude that the wavelength, \(\lambda\), is inversely proportional to \(k\).",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_3)
        else:
             textbox_4 = Tex(
                r"Concluímos que o comprimento de onda, \(\lambda\), é inversamente proporcional a \(k\).",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_3)
        self.play(Transform(textbox_1, textbox_4))

        eq5 = MathTex("\\lambda","=","\\frac{2\\pi}{k}")
        eq5.next_to(textbox_4, DOWN)
        self.play(Write(eq5))

        if lang == "eng":
            textbox_5 = Tex(
                r"The term \(k\) is known as the wave number; it expresses the \\"
                r"number of complete cycles that the wave has in an interval of \(2\pi\).",
                font_size=40,
                color=WHITE,
            ).next_to(eq5, DOWN)
        else:
             textbox_5 = Tex(
                r"O fator \(k\) é conhecido como número de onda, ele expressa o \\" 
                r"número de ciclos completos que a onda tem num intervalo de \(2\pi\).",
                font_size=40,
                color=WHITE,
            ).next_to(eq5, DOWN)
        self.play(Write(textbox_5))

        self.wait(6)

        eq6 = eq5.copy()
        eq7 = MathTex("k","=","\\frac{2\\pi}{\\lambda}")
        eq7.next_to(textbox_5, DOWN)
        self.play(TransformMatchingTex(eq6, eq7))

        self.wait(3)

    def slide_3(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The amplitude", font_size=48)
        else:
            title = Text("A amplitude", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Note that in the cases seen, the amplitude of the wave, that is, the \\"
                r"maximum distance the wave reaches on the \(y\)-axis from the \(x\)-axis, \\"
                r"is \(y\)=1. It is possible to modify this amplitude by multiplying the \\"
                r"cosine by a constant, \(A\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
             textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Note que nos casos vistos a amplitude da onda, isto é, a distância \\"
                r"máxima que a onda atinge no eixo \(y\) a partir do eixo \(x\) é \(y=1\). \\"
                r"É possível modificar essa amplitude multiplicando o cosseno por uma \\"
                r"constante, \(A\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        textbox_1.next_to(title, DOWN, buff=0.5)

        grafico1 = self.onda(k=2).scale(0.7).next_to(textbox_1, DOWN, aligned_edge=RIGHT)

        line_graph1 = grafico1[0].plot_line_graph(
            x_values = [PI, PI],
            y_values = [0, 1],
            vertex_dot_style={"fill_color": GREEN},
            line_color=RED,
            stroke_width = 2
        )
                
        eq1 =  MathTex("f(x)","=","cos","(kx)")
        eq1.next_to(textbox_1, DOWN, aligned_edge=LEFT)
        eq2 = MathTex("k","=","2")
        eq2.next_to(eq1, DOWN, aligned_edge=LEFT)

        textbox_2 = Tex("amplitude").scale(0.5).next_to(line_graph1, RIGHT, buff=0.05)

        self.add(grafico1, eq1, eq2, line_graph1, textbox_2)
        self.play(Write(textbox_1))

        self.wait(10)
           
        eq3 = MathTex("f(x)","=","A","cos","(kx)").move_to(eq1, aligned_edge=LEFT)
        eq4 = MathTex("A","=","1").next_to(eq2, DOWN, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq1, eq3), Write(eq4))

        if lang == "eng":
            textbox_3 = Tex(
                r"\begin{flushleft}"
                r"When \(A=1\), the amplitude is the original of the cosine. However, \\"
                r"when, for example, \(A=2\), we notice that the amplitude doubles. \\"
                r"Note that the wavelength, however, is not affected by \(A\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
        else:
             textbox_3 = Tex(
                r"\begin{flushleft}"
                r"Quando \(A=1\) a amplitude é a original do cosseno. Porém, quando, \\"
                r"por exemplo, \(A=2\) percebemos que a amplitude dobra. Note que o \\"
                r"comprimento de onda, porém, não é afetado por \(A\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
             
        self.play(Transform(textbox_1, textbox_3))

        self.wait(9)

        eq5 = MathTex("A","=","2")
        eq5.move_to(eq4, aligned_edge=LEFT)
        self.play(Transform(eq4, eq5))

        grafico2 = self.onda(A=2, k=2).scale(0.7).move_to(grafico1)

        line_graph2 = grafico2[0].plot_line_graph(
            x_values = [PI, PI],
            y_values = [0,2],
            vertex_dot_style={"fill_color": GREEN},
            line_color=RED,
            stroke_width = 2
        )

        self.play(
                TransformMatchingShapes(grafico1, grafico2),
                TransformMatchingShapes(line_graph1, line_graph2),
                textbox_2.animate.next_to(line_graph2, RIGHT, buff=0.05)
                )
        
        self.wait(3)
    
    def slide_4(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The velocity", font_size=48)
        else:
            title = Text("A velocidade ", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Suppose now that we want to shift the wave to the left or \\"
                r"to the right, keeping the same wavelength, but with the \\"
                r"maxima at different positions from the original ones. For \\"
                r"this, we can add a constant, \(c\), to the variable \(x\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
             textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Suponha agora que queiramos deslocar a onda para a esquerda ou \\"
                r"para a direita, mantendo o mesmo comprimento de onda, mas com \\"
                r"os máximos em posições diferentes das originais no eixo \(x\). \\"
                r"Para isso podemos somar uma constante, \(c\), à variável \(x\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        textbox_1.next_to(title, DOWN, buff=0.5)

        grafico1 = self.onda(A=1.5, k=2).scale(0.65).next_to(textbox_1, DOWN, aligned_edge=RIGHT)
                      
        eq1 =  MathTex("f(x)","=","A","cos","(kx)")
        eq1.next_to(textbox_1, DOWN, aligned_edge=LEFT)
        eq2 = MathTex("A","=","1.5")
        eq2.next_to(eq1, DOWN, aligned_edge=LEFT)
        eq3 = MathTex("k","=","2")
        eq3.next_to(eq2, DOWN, aligned_edge=LEFT)

        self.add(grafico1, eq1, eq2, eq3)
        self.play(Write(textbox_1))

        self.wait(12)
           
        eq4 = MathTex("f(x)","=","A","cos","[k(x+c)]").move_to(eq1, aligned_edge=LEFT)
        eq5 = MathTex("c","=","0").next_to(eq3, DOWN, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq1, eq4), Write(eq5))

        self.wait(3)

        if lang == "eng":
            textbox_2 = Tex(
                r"\begin{flushleft}"
                r"If we set \(c=\pi/4\), we notice that the maxima of \\"
                r"the function shift \(-\pi/4\) (to the left), without \\"
                r"changing the amplitude or the wavelength."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
        else:
             textbox_2 = Tex(
                r"\begin{flushleft}"
                r"Se fizermos \(c=\pi/4\) notamos que os máximos da função \\"
                r"se deslocam \(-\pi/4\) (para a esquerda), mas sem alterar a \\"
                r"amplitude ou o comprimento da onda."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_1)
             
        self.play(TransformMatchingTex(textbox_1, textbox_2))

        self.wait(8)

        eq6 = MathTex("c","=","\\pi/4")
        eq6.move_to(eq5, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq5, eq6))

        grafico2 = self.onda(A=1.5, k=2, d=PI/2).scale(0.65).move_to(grafico1, aligned_edge=DOWN)

        self.play(TransformMatchingShapes(grafico1, grafico2))

        self.wait(3)
        
        if lang == "eng":
            textbox_3 = Tex(
                r"\begin{flushleft}"
                r"The parameter \(c\) can be used to shift the wave along the \(x\) axis with \\"
                r"the evolution of time, \(t\), and according to a given velocity, \(v\). \\"
                r"We can use the well-known linear motion equation: \(c=vt\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_2)
        else:
             textbox_3 = Tex(
                r"\begin{flushleft}"
                r"O parâmetro \(c\) pode ser usado para deslocar a onda no eixo \(x\) com a \\"
                r"evolução do tempo, \(t\), e de acordo com uma dada velocidade, \(v\). \\"
                r"Podemos usar a conhecida equação do movimento linear: \(c=vt\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_2)
        self.play(ReplacementTransform(textbox_2, textbox_3))

        self.wait(9)

        eq4[4][5].set_color(YELLOW)

        eq7 = MathTex("f(x,t)","=","A","cos","[k(x+vt)]").move_to(eq4, aligned_edge=LEFT)
        eq8 = MathTex("c=vt").next_to(textbox_3, DOWN).set_color(YELLOW)
        eq9 = MathTex("v","=","\\pi/s").move_to(eq6, aligned_edge=LEFT)

        self.add(eq8)
        self.play(
            eq8.animate.move_to(eq4, aligned_edge=RIGHT).scale(0),
            TransformMatchingTex(eq4, eq7),
            ReplacementTransform(eq6, eq9),
            run_time=3
        )

        tracker=ValueTracker(0)
        grafico3 = always_redraw (lambda:
            self.onda(A=1.5, k=2, w=-2*PI, t=tracker.get_value()).scale(0.65).move_to(grafico2)
        )
        
        self.replace(grafico2, grafico3)

        self.play(
            tracker.animate.set_value(10), 
            rate_func= linear, 
            run_time=5
            )
        
        if lang == "eng":
            textbox_4 = Tex(
                r"\begin{flushleft}"
                r"Note that when the velocity is positive, the wave shifts to the \\"
                r"left, so if we want the wave to move in the same direction \\"
                r"as the velocity, we need to multiply \(vt\) by \(-1\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_2)
        else:
             textbox_4 = Tex(
                r"\begin{flushleft}"
                r"Note que quando a velocidade é positiva a onda se desloca para a \\"
                r"esquerda, assim, se desejamos que a onda se desloque no mesmo \\"
                r"sentido da velocidade precisamos multiplicar \(vt\) por \(-1\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).move_to(textbox_2)
                 
        self.replace(textbox_3, textbox_4)
        
        tracker.set_value(0)
        self.play(
            tracker.animate.set_value(12), 
            rate_func = linear, 
            run_time = 9
            )
        
        eq4[4][4].set_color(YELLOW)

        eq10 = MathTex("(-1)").next_to(textbox_4, DOWN).set_color(YELLOW)
        eq11 = MathTex("f(x,t)","=","A","cos","[k(x-vt)]").move_to(eq7, aligned_edge=LEFT)

        tracker.update(0)
        self.play(
            eq10.animate.move_to(eq7, aligned_edge=RIGHT).scale(0),
            TransformMatchingTex(eq7, eq11),
            rate_func = linear
        )

        grafico4 = always_redraw (lambda:
            self.onda(A=1.5, k=2, w=2*PI, t=tracker.get_value()).scale(0.65).move_to(grafico3)
        )

        self.remove(grafico3)
        self.add(grafico4)

        tracker.set_value(0)
        self.play(
            tracker.animate.set_value(10), 
            rate_func = linear, 
            run_time = 6
            )
   
    def slide_5(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The phase constant", font_size=48)
        else:
            title = Text("A constante de fase", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Note, however, that, in its current form, the wave function \\"
                r"will always have a maximum at \(x=0\) for \(t=0\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        else:
             textbox_1 = Tex(
                r"\begin{flushleft}"
                r"Note, contudo, que, na forma em que está a função da \\"
                r"onda sempre terá um máximo em \(x=0\) para \(t=0\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            )
        textbox_1.next_to(title, DOWN, buff=0.5)

        eq1 = MathTex("f(x,t)","=","A","cos","[k(x-vt)]").next_to(textbox_1, DOWN)

        self.play(Write(textbox_1), Write(eq1))

        self.wait(6)

        eq2 = MathTex("f(0,0)","=","A","cos","[k(0-v0)]").move_to(eq1, aligned_edge=LEFT)
        eq2[0][2].set_color(YELLOW)
        eq2[0][4].set_color(YELLOW)
        eq2[4][3].set_color(YELLOW)
        eq2[4][6].set_color(YELLOW)
        self.play(TransformMatchingTex(eq1, eq2))
        self.wait(4)
        eq3 = MathTex("f(0,0)","=","A","cos","[0]").move_to(eq2, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq2, eq3))
        self.wait(4)
        eq4 = MathTex("f(0,0)","=","A","1").move_to(eq3, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq3, eq4))
        self.wait(4)
        eq5 = MathTex("f(0,0)","=","A").move_to(eq4, aligned_edge=LEFT)
        self.play(TransformMatchingTex(eq4, eq5))
        self.wait(4)

        self.play(Unwrite(eq5))

        if lang == "eng":
            textbox_2 = Tex(
                r"\begin{flushleft}"
                r"Suppose now that we want the wave at \(t=0\) to start shifted \\"
                r"from the original, that is, not with its maximum at \(x=0\). \\"
                r"In this case, we just need to add a constant to the entire set \\"
                r"inside the cosine, which shifts the wave at the beginning. This \\"
                r"constant is called the phase constant, \(\delta\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).next_to(title, DOWN, buff=0.5)
        else:
             textbox_2 = Tex(
                r"\begin{flushleft}"
                r"Suponha agora que desejamos que em \(t=0\) a onda deverá começar \\"
                r"defasada da original, isto é, não com o seu máximo em \(x=0\). \\"
                r"Neste caso basta somarmos ao conjunto todo, dentro do cosseno, \\"
                r"uma constante que desloca a onda no início, isto é, para \(t=0\). \\"
                r"Essa constante é chamada de constante de fase, \(\delta\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).next_to(title, DOWN, buff=0.5)
             
        self.play(Transform(textbox_1, textbox_2))

        eq1.next_to(textbox_2, DOWN,buff=0.5)
        self.play(Write(eq1))

        self.wait(15)

        eq2 = MathTex("f(x,t)","=","A","cos","[k(x-vt)+\\delta]").move_to(eq1, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq1, eq2))

        self.wait(4)

        if lang == "eng":
            textbox_3 = Tex(
                r"\begin{flushleft}"
                r"See this example with a phase shift of \(-\pi/4\). In this case, \(\delta=\pi/2\) \\"
                r"because the phase shift will always correspond to \(-\delta/k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).next_to(title, DOWN, buff=0.5)
        else:
             textbox_3 = Tex(
                r"\begin{flushleft}"
                r"Veja esse exemplo com uma defasagem de \(-\pi/4\). Neste caso \\"
                r"\(\delta=\pi/2\) pois a defasagem sempre corresponderá a \(-\delta/k\)."
                r"\end{flushleft}",
                font_size=40,
                color=WHITE,
            ).next_to(title, DOWN, buff=0.5)
             
        self.play(
                Transform(textbox_1, textbox_3),
                eq2.animate.next_to(textbox_3, DOWN, aligned_edge=LEFT)
        )

        self.wait(4)

        eq3 = MathTex("f(x,0)","=","1.5","cos","[2(x-3t)+\\pi/2]").move_to(eq2, aligned_edge=LEFT)
        grafico1 = self.onda(A=1.5,k=2,d=PI/2).scale(0.7).next_to(eq2, DOWN, aligned_edge=LEFT)

        self.play(
                TransformMatchingTex(eq2, eq3),
                Create(grafico1)
        )

        self.wait(4)

    def slide_6(self):

            # padrão
            self.slide_pattern()

            # Add the title
            if lang=='eng':
                title = Text("The angular frequency", font_size=48)
            else:
                title = Text("A frequência angular", font_size=48)
            title.to_edge(UP)
            self.play(Write(title))

            self.wait()
            
            separation_line = Line(
                start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
                end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
                color=BLUE_D
            )
            self.play(Create(separation_line))

            self.wait()

            if lang == "eng":
                textbox_1 = Tex(
                    r"\begin{flushleft}"
                    r"We thus have a generic function capable of describing \\"
                    r"the time displacement of any sinusoidal wave."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                )
            else:
                textbox_1 = Tex(
                    r"\begin{flushleft}"
                    r"Temos assim uma função genérica capaz de descrever o deslocamento \\"
                    r"no tempo de qualquer onda do tipo senoidal."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                )
            textbox_1.next_to(title, DOWN, buff=0.5)

            eq1 = MathTex("f(x,t)","=","A","cos","[k(x-vt)+\delta]").next_to(textbox_1, DOWN, buff=0.5)

            self.play(Write(textbox_1), Write(eq1))

            self.wait(6)

            if lang == "eng":
                textbox_2 = Tex(
                    r"\begin{flushleft}"
                    r"The time required for the wave to complete one cycle is called \\"
                    r"the period, \(T\). It can be easily calculated. Just remember that \\"
                    r"a complete cycle of the wave occurs for its wavelength, \(\lambda\). If \\"
                    r"we divide this length by the wave's propagation speed, \(v\), we \\"
                    r"will then have its period."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).next_to(eq1, DOWN, buff=0.5)
            else:
                textbox_2 = Tex(
                    r"\begin{flushleft}"
                    r"O tempo necessário para que a onda complete um ciclo é chamado \\"
                    r"de período, \(T\). Ele pode ser facilmente calculado. Basta lembrar que \\"
                    r"um ciclo completo da onda ocorre para seu comprimento de onda, \(\lambda\). \\"
                    r"Se dividirmos esse comprimento pela velocidade de deslocamento da \\"
                    r"onda, \(v\), teremos, então, seu período."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).next_to(eq1, DOWN, buff=0.5)
            self.play(Write(textbox_2))

            eq3 = MathTex("T","=","\\frac{\\lambda}{v}").next_to(textbox_2, DOWN)
            self.play(Write(eq3))
                
            self.wait(14)

            eq4 = MathTex("\\lambda=\\frac{2\\pi}{k}").set_color(YELLOW).next_to(eq3, RIGHT, buff=1)
            eq3[2][0].set_color(YELLOW)

            self.play(Write(eq4))

            self.wait(4)

            eq5 = MathTex("T","=","\\frac{2\\pi}{kv}").move_to(eq3, aligned_edge=LEFT)

            self.play(
                    eq4.animate.move_to(eq3, LEFT).scale(0),
                    TransformMatchingTex(eq3, eq5)
            )

            self.wait(4)

            if lang == "eng":
                textbox_3 = Tex(
                    r"\begin{flushleft}"
                    r"The frequency of the wave, \(\nu\), is the number of complete cycles per \\"
                    r"unit of time and will be exactly equal to the inverse of its period."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_2)
            else:
                textbox_3 = Tex(
                    r"\begin{flushleft}"
                    r"A freqüência da onda, \(\nu\), é número de ciclos completos por unidade\\"
                    r"de tempo e será exatamente igual ao inverso do seu período."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_2)
            self.play(ReplacementTransform(textbox_2, textbox_3))

            self.wait(6)

            eq6 = MathTex("\\nu","=","\\frac{1}{T}","=","\\frac{kv}{2\\pi}").move_to(eq5, aligned_edge=RIGHT)
            self.play(TransformMatchingTex(eq5, eq6))

            self.wait(4)

            eq7 = MathTex("\\nu","=","\\frac{kv}{2\\pi}").move_to(eq6, aligned_edge=LEFT)
            self.play(TransformMatchingTex(eq6, eq7))

            self.wait(4)

            self.play(
                Unwrite(textbox_3),
                eq7.animate.shift(LEFT*3)
            )

            self.wait(4)

            if lang == "eng":
                textbox_4 = Tex(
                    r"\begin{flushleft}"
                    r"From circular motion, we know that the angular frequency, \(\omega\), \\"
                    r"is the number of radians per unit of time and is given by:"
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_3)
            else:
                textbox_4 = Tex(
                    r"\begin{flushleft}"
                    r"Do movimento circular, sabemos que a freqüência angular, \(\omega\), \\"
                    r"é o número de radianos por unidade de tempo e é dada por:"
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_3)

            eq8 = MathTex("\\omega","=","2","\\pi","\\nu").next_to(textbox_4, DOWN)

            self.play(
                    Write(textbox_4),
                    Write(eq8)
            )

            self.wait(6)

            eq9 = MathTex("\\omega","=","2","\\pi","\\frac{kv}{2\\pi}").move_to(eq8, aligned_edge=LEFT)

            self.play(Unwrite(textbox_4))
            eq8[4].set_color(YELLOW)
            eq7.set_color(YELLOW)

            self.wait(4)

            self.play(
                    eq7.animate.move_to(eq8[4]).scale(0),
                    TransformMatchingTex(eq8, eq9)
            )

            self.wait(4)

            eq9[2:4].set_color(YELLOW)
            eq9[4][3:].set_color(YELLOW)

            self.wait(4)

            self.play(
                eq9[2:4].animate.scale(0),
                eq9[4][2:].animate.scale(0)
            )

            eq10 = MathTex("\\omega","=","k","v").move_to(eq9, aligned_edge=LEFT)
            self.play(TransformMatchingTex(eq9, eq10))

            self.wait(4)

            if lang == "eng":
                textbox_5 = Tex(
                    r"\begin{flushleft}"
                    r"It is more convenient to represent the wave function in terms \\"
                    r"of its angular frequency rather than its propagation speed."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_1)
            else:
                textbox_5 = Tex(
                    r"\begin{flushleft}"
                    r"É mais conveniente representar a função da onda em relação à sua \\"
                    r"freqüência angular do que de sua velocidade de deslocamento."
                    r"\end{flushleft}",
                    font_size=40,
                    color=WHITE,
                ).move_to(textbox_1)
            self.play(Transform(textbox_1, textbox_5))

            self.wait(6)

            eq11 = MathTex("v","=","\\frac{\\omega}{k}").move_to(eq10)
            self.play(TransformMatchingTex(eq10, eq11))

            self.wait(4)
            eq1[4][5].set_color(YELLOW)
            eq11.set_color(YELLOW)

            self.wait(4)

            eq12 = MathTex("f(x,t)","=","A","cos","[k(x-\\frac{\\omega}{k}t)+\\delta]").move_to(eq1, aligned_edge=LEFT)

            self.play(
                    eq11.animate.move_to(eq1[4][5]).scale(0),
                    TransformMatchingTex(eq1, eq12)
            )

            self.wait(4)

            eq13 = MathTex("f(x,t)","=","A","cos","(kx-k\\frac{\\omega}{k}t+\\delta)").move_to(eq12, aligned_edge=LEFT)
            self.play(TransformMatchingTex(eq12, eq13))

            self.wait(4)
            eq13[4][4].set_color(YELLOW)
            eq13[4][7].set_color(YELLOW)

            self.wait(4)

            eq14 = MathTex("f(x,t)","=","A","cos","(kx-\\omega t+\\delta)").move_to(eq13, aligned_edge=LEFT)
            self.play(
                    eq13[4][4].animate.scale(0),
                    eq13[4][6:8].animate.scale(0)       
            )

            self.play(TransformMatchingTex(eq13, eq14))

            self.wait(4)
        
    def slide_7(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("The uniform plane wave", font_size=48)
        else:
            title = Text("A onda plana e uniforme", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
            
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Text(
                "IMPORTANT: Although our wave has been represented in a Cartesian plane, \n"
                "this does not make it a plane wave. In a plane wave, the amplitude, \n"
                "orientation, and phase depend solely on the direction of propagation. \n"
                "Given a plane perpendicular to the direction of propagation, all these \n"
                "properties are the same in this plane. Furthermore, in our case, since \n"
                "the amplitude is constant, we say that the wave is uniform.",
                font_size=24, line_spacing=1.5
            )
        else:
            textbox_1 = Text(
                "IMPORTANTE: Embora nossa onda tenha sido representada num plano \n"
                "cartesiano, não é por isso que ela é uma onda plana. Numa onda plana, \n"
                "a amplitude, a orientação e a fase só dependem da direção de propagação. \n"
                "Dado um plano perpendicular à direção de propagação todas essas \n"
                "propriedades são as mesmas neste plano. Além disso, em nosso caso, \n"
                "como a amplitude é constante, dizemos que a onda é uniforme.",
                font_size=24, line_spacing=1.5
            )
        
        self.play(Write(textbox_1))

        self.wait(18)

        self.play(Unwrite(textbox_1))

        tracker = ValueTracker(0)

        # Configurar os eixos
        axes = Axes(
            x_range=[-2*PI, 2*PI, PI/4],  # Limites para o eixo x
            y_range=[-2, 2, 0.5],  # Limites para o eixo y
        )

        axes.next_to(separation_line, DOWN, buff=0.5)

        # Definir a função de onda senoide para o campo vetorial no plano yz
        def sine_wave_field(pos):
            t = tracker.get_value()
            x, y, z = pos
            field = np.array([0, 2*np.cos(x-t), 0])
            return field
        
                  
        vector_field = always_redraw(lambda: 
            ArrowVectorField(
                sine_wave_field,
                x_range=[-2*PI, 2*PI, PI/8],  # Única camada no plano yz
                y_range=[-2, 2, 0.5],
                z_range=[-1,1,0.5],
            ).next_to(separation_line, DOWN, buff=1)
        )
        
        cos_graph = always_redraw(lambda:
                                  axes.plot(lambda x: np.cos(x-tracker.get_value()), color=WHITE)
                    )
                    
        self.add(vector_field, cos_graph)

        self.play(
            tracker.animate.set_value(20), 
            run_time=10, 
            rate_func=linear
        )
          
    def slide_8(self):

        # padrão
        self.slide_pattern()

        # Add the title
        if lang=='eng':
            title = Text("Exponential form", font_size=48)
        else:
            title = Text("Forma exponencial", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
            
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        self.wait()

        if lang == "eng":
            textbox_1 = Text(
                "A plane and uniform wave function can be represented by an exponential \n"
                "function, which greatly simplifies calculations, as differentiating or \n"
                "integrating sines or cosines is more complicated. This representation \n"
                "stems from the famous Euler's formula.",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_1 = Text(
                "A função da onda plana e uniforme pode ser representada por uma função \n"
                "exponencial, o que facilita muito os cálculos, pois derivar ou integrar \n"
                "senos ou cossenos é mais complicado. Essa representação parte da \n"
                "famosa fórmula de Euler.",
                font_size=24, line_spacing=1.05
            )
        textbox_1.next_to(separation_line, DOWN)
        
        self.play(Write(textbox_1))

        self.wait(8)

        if lang == 'eng':
            eq1 =  MathTex("e^","{i","\\phi}","=","cos","(\\phi)","+","i","sin","(\\phi)")
        else:
            eq1 =  MathTex("e^","{i","\\phi}","=","cos","(\\phi)","+","i","sen","(\\phi)")
        eq1.next_to(textbox_1, DOWN, buff=0.5)

        self.play(Write(eq1))

        self.wait(4)

        if lang == "eng":
            textbox_2 = Tex(
                r"\begin{flushleft}"
                r"\(e\) is the Napier's constant \\"
                r"\(i\) is the imaginary unit, \(\sqrt{-1}\) \\"
                r"\(\phi\) is any real number"
                r"\end{flushleft}",
                font_size=40,
                )
        else:
            textbox_2 = Tex(
                r"\begin{flushleft}"
                r"\(e\) é o número neperiano \\"
                r"\(i\) é o número imaginário, \(\sqrt{-1}\) \\"
                r"\(\phi\) é um número real qualquer"
                r"\end{flushleft}",
                font_size=40,
                )
        textbox_2.next_to(eq1, DOWN, buff=0.5)
        self.play(Write(textbox_2))

        self.wait(6)

        if lang == "eng":
            textbox_3 = Text(
                "This relation can be easily understood by placing the unit trigonometric \n"
                "circle in the complex plane. The real axis represents the cosines and the \n"
                "imaginary axis represents the sines.",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_3 = Text(
                "Essa relação pode ser facilmente entendida colocando o círculo \n"
                "trigonométrico no plano complexo. O eixo real representa os \n"
                "cossenos o eixo imaginário representa os senos.",
                font_size=24, line_spacing=1.05
            )
        textbox_3.move_to(textbox_1)
        self.play(ReplacementTransform(textbox_1, textbox_3))

        self.wait(9)

        self.play(Unwrite(textbox_2))
        self.play(eq1.animate.next_to(textbox_3, DOWN, buff=0.5).shift(RIGHT))
       
        # Configurar os eixos
        axes = Axes(
            x_range=[-1.3, 1.3, 1],  # Limites para o eixo x
            y_range=[-1.3, 1.3, 1],  # Limites para o eixo y
            x_length = 4.5,
            y_length = 4.5,
            axis_config ={'tip_height':0.2, 'tip_width':0.1},
            x_axis_config={"include_numbers": True,
                           "numbers_to_include": list(range(-1,2,1)),
                           "decimal_number_config": {"num_decimal_places": 0,},
                           "font_size":24,
                           "label_direction":np.array([-0.5,-0.5,0])
            },
            y_axis_config={"label_direction":np.array([-0.5,0.5,0])}
        )

        axis_labels = axes.get_axis_labels(x_label=Tex('Re').scale(0.5), y_label=Tex('Im').scale(0.5))

        # Definição dos rótulos personalizados
        y_labels = {
            -1: MathTex("-i"),
             1: MathTex("i"),
        }

        # Adiciona os rótulos aos eixos
        for y, label in y_labels.items():
            axes.get_y_axis().add_labels({y: label})

        circle = axes.plot_parametric_curve(
            lambda t: 
            np.array([np.cos(t), np.sin(t),0]),
            t_range = [0, 2 * PI],
            color = RED
            )
        
        arco = axes.plot_parametric_curve(
            lambda t: 
            np.array([0.2*np.cos(t), 0.2*np.sin(t),0]),
            t_range = [0, PI/3],
            )
        
        vetor = axes.plot_line_graph([0,np.cos(PI/3)], [0,np.sin(PI/3)], add_vertex_dots=False)
        vetor_x = axes.plot_line_graph([0,np.cos(PI/3)], [0,0], add_vertex_dots=False, line_color=GREEN_E)
        vetor_y = axes.plot_line_graph([0,0], [0,np.sin(PI/3)], add_vertex_dots=False, line_color=BLUE_D)
        v_conect =  axes.plot_line_graph([0,np.cos(PI/3),np.cos(PI/3)],[np.sin(PI/3),np.sin(PI/3),0], add_vertex_dots=False, line_color=WHITE)
        v_conect.set_stroke(width=1)
                
        ang_label = MathTex("\\phi").scale(0.7).next_to(arco, UR, buff=0)
        vet_x_lable = MathTex("cos(\\phi)").scale(0.6).next_to(vetor_x, DOWN, buff=0.1)
        if lang == 'eng':
            vet_y_lable = MathTex("sin(\\phi)").scale(0.6).next_to(vetor_y, LEFT, buff=0.1)
        else:
            vet_y_lable = MathTex("sen(\\phi)").scale(0.6).next_to(vetor_y, LEFT, buff=0.1)
        
        grupo = VGroup(axes, axis_labels, 
                       circle, arco, ang_label, 
                       vetor, vetor_x, vet_x_lable, 
                       vetor_y, vet_y_lable, v_conect).next_to(textbox_1, DOWN, aligned_edge=LEFT)

        self.play(Create(grupo))

        self.wait(4)

        if lang == "eng":
            textbox_4 = Tex(
                r"\begin{flushleft}"
                r"Note that the real number \(\phi\) corresponds to an angle on the unit \\"
                r"trigonometric circle. For any real number \(\phi\), \(e^{i\phi}\) always \\"
                r"produces a complex number with the real part between -1 and 1, \\"
                r"and the imaginary part between \(-i\) and \(i\)."
                r"\end{flushleft}",
                font_size=36,
                )
        else:
            textbox_4 = Tex(
                r"\begin{flushleft}"
               r"Note que o número real \(\phi\) corresponde a um ângulo no círculo \\"
                r"trigonométrico. Para qualquer número real \(\phi\),  \(e^{i\phi}\) sempre \\"
                r"produzirá um número complexo com a parte real entre -1 e 1, \\"
                r"e a parte imaginária entre \(-i\) e \(i\)."
                r"\end{flushleft}",
                font_size=36,
                )
        textbox_4.move_to(textbox_3)
        self.play(FadeOut(textbox_3))
        self.play(Write(textbox_4))

        self.wait(12)

        if lang == "eng":
            textbox_5 = Text(
                "With Euler's formula, we can transform our wave function, \n"
                "which uses cosine, into an exponential function.",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_5 = Text(
                "Com a fórmula de Euler podemos transformar nossa função de onda, \n"
                "que usa cosseno, em uma função exponencial.",
                font_size=24, line_spacing=1.05
            )
        textbox_5.move_to(textbox_4)

        self.play(FadeOut(grupo), eq1.animate.move_to(LEFT), FadeOut(textbox_4))
        self.play(Write(textbox_5))

        eq2 = MathTex("f(x,t)","=","A","cos(","kx-\omega t+\delta",")")
        eq2.next_to(eq1, DOWN, buff=1)
        
        self.play(Write(eq2))

        self.wait(4)

        eq1[2].set_color(YELLOW)
        eq1[5][1].set_color(YELLOW)
        eq1[9][1].set_color(YELLOW)

        eq2[4].set_color(YELLOW)
        eq2[2].set_color(YELLOW)

        if lang=='eng':        
            eq3 = MathTex("A","e^","{i","(kx-\omega t+\delta)}","=","A","cos","(kx-\omega t+\delta)","+","A","i","sin","(kx-\omega t+\delta)")
        else:
            eq3 = MathTex("A","e^","{i","(kx-\omega t+\delta)}","=","A","cos","(kx-\omega t+\delta)","+","A","i","sen","(kx-\omega t+\delta)")
        eq3[3].set_color(YELLOW)
        eq3[7][1:8].set_color(YELLOW)
        eq3[12][1:8].set_color(YELLOW)
        eq3[0].set_color(YELLOW)
        eq3[5].set_color(YELLOW)
        eq3[9].set_color(YELLOW)
        eq3.move_to(eq1).shift(RIGHT)

        self.wait(4)

        self.play(
            eq2[4].copy().animate.move_to(eq1[2]).scale(0),
            eq2[4].copy().animate.move_to(eq1[5]).scale(0),
            eq2[4].copy().animate.move_to(eq1[9]).scale(0),
            eq2[2].copy().animate.move_to(eq1[0]).scale(0),
            eq2[2].copy().animate.move_to(eq1[4]).scale(0),
            eq2[2].copy().animate.move_to(eq1[8]).scale(0),
            TransformMatchingTex(eq1, eq3)
        )

        self.wait(4)

        self.play(
            FadeOut(eq2),
            eq3.animate.set_color(WHITE)
            )
        
        self.wait(4)
        
        if lang == "eng":
            textbox_6 = Text(
                "Note that if we take only the real part produced by the exponential \n"
                "function, we will have exactly the original wave function.",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_6 = Text(
                "Note que, se tomarmos só a parte real produzida pela função \n"
                "exponencial teremos exatamente a função de onda original.",
                font_size=24, line_spacing=1.05
            )
        textbox_6.next_to(eq3, DOWN, buff=0.5)

        self.play(Write(textbox_6))

        self.wait(4)

        eq4 = MathTex("f(x,t)=Re[Ae^{i(kx-\omega t+\delta)}]=Acos(kx-\omega t+\delta)")
        eq4.next_to(textbox_6, DOWN)

        self.play(Write(eq4))

        self.wait(4)

        if lang == "eng":
            textbox_7 = Text(
                "We can, therefore, work with the exponential form of the wave, \n"
                "and when necessary, extract only the real part of the result.",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_7 = Text(
                "Podemos, portanto, trabalhar com a forma exponencial da onda e, \n"
                "quando necessário, extraímos só a parte real do resultado.",
                font_size=24, line_spacing=1.05
            )
        textbox_7.move_to(textbox_6)

        self.play(Transform(textbox_6, textbox_7), FadeOut(eq4))

        self.wait(4)

        eq5 = MathTex("\psi","=","A","e^","{i","(kx","-\omega t","+\delta)","}")
        eq5.move_to(eq3)

        self.play(TransformMatchingTex(eq3, eq5), FadeOut(textbox_6), FadeOut(textbox_5))

        self.wait(4)

        if lang == "eng":
            textbox_8 = Text(
                "Simplifying",
                font_size=24, line_spacing=1.05
            )
        else:
            textbox_8 = Text(
                "Simplificando",
                font_size=24, line_spacing=1.05
            )
        textbox_8.next_to(eq5, UP, buff=1)

        self.play(Write(textbox_8))

        self.wait(4)

        eq6 = MathTex("\psi","=","Ae^{i\delta}","e^","{i","(kx","-\omega t)","}")
        self.play(TransformMatchingTex(eq5, eq6))

        self.wait(4)

        if lang=='eng':
            text_eq7 =  Tex(r"Let's make ")
        else:
            text_eq7 =  Tex(r"Vamos fazer ")
        text_eq7.next_to(eq6, DOWN, buff=1.5)    
        eq7 = MathTex("C=Ae^{i\delta}")
        eq7.next_to(text_eq7, RIGHT)

        self.play(Write(text_eq7), Write(eq7))

        self.wait(4)

        eq6[2].set_color(YELLOW)
        eq7.set_color(YELLOW)

        self.wait(4)

        eq8 = MathTex("\psi","=","C","e^","{i","(kx","-\omega t)","}")
        eq8.move_to(eq6, aligned_edge=LEFT)

        self.play(
            eq7.animate.move_to(eq6[2]).scale(0),
            FadeOut(text_eq7),
            TransformMatchingTex(eq6, eq8),
            FadeOut(textbox_8)
        )

if __name__ == "__main__":

    #language
    lang= 'eng'
    #lang = 'port'

    config.quality = "medium_quality"

    if lang=='eng':
        config.output_file="plane_wave_function.mp4"
    else:
        config.output_file="funcao_onda_plana.mp4"
    
    scene = plane_wave_function()
    scene.render()

        

        
    

   