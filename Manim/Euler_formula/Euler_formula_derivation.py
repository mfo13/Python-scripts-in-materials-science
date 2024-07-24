"""
Euler's formula derivation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It produces a mp4 movie explaining the Euler's formula derivation
from Taylor series.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for undergrad students.

Packages needed:
manim
ps.: must have Latex in your system

Usage:
$ Euler_formula_derivation.py

You can choose between english or portuguese (Brazil)
by setting the variable 'lang' in the #Main

Date: July/2024
Version: 1.0
"""

from manim import *

class Euler_formula_derivation(Scene):
    def construct(self):
        
        self.cover()
        self.wait(3)
        
        self.remove(*self.mobjects)
        self.slide_1()
        self.wait(3)
               
    def Euler_circle(self):
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

        eu = MathTex("e^{i\phi}")
        eu.next_to(vetor, UR, buff=0.1)

        completo = VGroup(axes, axis_labels, 
                       circle, arco, ang_label, 
                       vetor, vetor_x, vet_x_lable, 
                       vetor_y, vet_y_lable, v_conect, eu)
                      
        simples = VGroup(axes, circle, arco,  
                       vetor, vetor_x, vetor_y, 
                       v_conect)

        return completo, simples
   
    def cover(self):
        figura, a = self.Euler_circle()
        figura.to_edge(LEFT).shift(RIGHT)
        self.play(Write(figura), run_time=6)

        if lang=="eng":
            title = Text("Euler's formula \n"
                         "derivation", font_size=48, line_spacing=1.5)
        else:
            title =  Text("Dedução da \n"
                          "fórmula de Euler", font_size=48, line_spacing=1.5)
        title.next_to(figura, RIGHT, buff=1)
        self.play(Write(title), run_time=2)
 
    def slide_1(self):

        # padrão
        a,figurinha = self.Euler_circle()
        figurinha.scale(0.3).to_corner(UL, buff=0.1)
        self.add(figurinha)

        # Add the title
        if lang=='eng':
            title = Text("Euler's formula", font_size=48)
        else:
            title = Text("A fórmula de Euler", font_size=48)
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
            eq1 = MathTex("e^","{ix}","=","cos(x)","+","i","sin(x)")
        else:
            eq1 = MathTex("e^","{ix}","=","cos(x)","+","i","sen(x)")
        eq1.next_to(separation_line, DOWN, buff=0.5)

        self.play(Write(eq1))

        self.wait(4)

        eq2 = MathTex("e^","x","=","\sum_{n=0}^{\infty}","{\\frac{1}{n!}","x","^n}")
        eq2.next_to(eq1, DOWN, buff=1)
        
        if lang=="eng":
            text_1 = Text("From Taylor series", font_size=28)
        else:
            text_1 = Text("Das séries de Taylor", font_size=28)
        text_1.next_to(eq2, RIGHT, buff=0.5)

        self.play(Write(eq2), Write(text_1))

        self.wait(4)

        self.play(Unwrite(text_1))

        eq1[1].set_color(YELLOW)
        eq2[1].set_color(YELLOW)
        eq2[5].set_color(YELLOW)

        self.wait(4)

        eq3 = MathTex("e^","{ix}","=","\sum_{n=0}^{\infty}","{\\frac{1}{n!}","(ix)","^n}")

        self.play(
            eq1[1].copy().animate.move_to(eq2[1]).scale(0),
            eq1[1].copy().animate.move_to(eq2[5]).scale(0),                              
            eq1[1].animate.set_color(WHITE),
            TransformMatchingTex(eq2, eq3)
            )
        
        self.wait(4)

        eq3[3:].set_color(YELLOW)

        self.wait(4)

        eq4 = MathTex("e^","{ix}","=","\\frac{1}{0!}","(ix)","^0","+",
                      "\\frac{1}{1!}","(ix)","^1","+",
                      "\\frac{1}{2!}","(ix)","^2","+",
                      "\\frac{1}{3!}","(ix)","^3","+",
                      "\\frac{1}{4!}","(ix)","^4","+",
                      "\\frac{1}{5!}","(ix)","^5","+",
                      "\\frac{1}{6!}","(ix)","^6","+",
                      "\\frac{1}{7!}","(ix)","^7","+",
                      "..."
                      )
        eq4.move_to(eq3).scale(0.7)

        self.play(TransformMatchingTex(eq3, eq4))

        self.wait(4)

        eq4[3:6].set_color(YELLOW)
        eq4[7:10].set_color(YELLOW)
        eq4[11].set_color(YELLOW)

        self.wait(4)
        
        eq5 = MathTex("e^","{ix}","=","1","+",
                      "ix","+",
                      "\\frac{1}{2}","(ix)","^2","+",
                      "\\frac{1}{3!}","(ix)","^3","+",
                      "\\frac{1}{4!}","(ix)","^4","+",
                      "\\frac{1}{5!}","(ix)","^5","+",
                      "\\frac{1}{6!}","(ix)","^6","+",
                      "\\frac{1}{7!}","(ix)","^7","+",
                      "..."
                      )
        eq5.scale(0.7).move_to(eq4, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4, eq5))

        self.wait(4)

        eq5[8:10].set_color(YELLOW)
        eq5[12:14].set_color(YELLOW)
        eq5[16:18].set_color(YELLOW)
        eq5[20:22].set_color(YELLOW)
        eq5[24:26].set_color(YELLOW)
        eq5[28:30].set_color(YELLOW)

        self.wait(4)

        eq6 = MathTex("e^","{ix}","=","1","+",
                      "ix","+",
                      "\\frac{1}{2}","i^2","x^2","+",
                      "\\frac{1}{3!}","i^3","x^3","+",
                      "\\frac{1}{4!}","i^4","x^4","+",
                      "\\frac{1}{5!}","i^5","x^5","+",
                      "\\frac{1}{6!}","i^6","x^6","+",
                      "\\frac{1}{7!}","i^7","x^7","+",
                      "..."
                      )
        eq6.scale(0.7).move_to(eq5, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5, eq6))

        self.wait(4)

        eq6[8].set_color(YELLOW)
        eq6[12].set_color(YELLOW)
        eq6[16].set_color(YELLOW)
        eq6[20].set_color(YELLOW)
        eq6[24].set_color(YELLOW)
        eq6[28].set_color(YELLOW)

        self.wait(4)

        eq7 = MathTex("e^","{ix}","=","1","+",
                      "ix","+",
                      "\\frac{1}{2}","(-1)","x^2","+",
                      "\\frac{1}{3!}","(-i)","x^3","+",
                      "\\frac{1}{4!}","1","x^4","+",
                      "\\frac{1}{5!}","i","x^5","+",
                      "\\frac{1}{6!}","(-1)","x^6","+",
                      "\\frac{1}{7!}","(-i)","x^7","+",
                      "..."
                      )
        eq7.scale(0.7).move_to(eq6, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq6, eq7))

        self.wait(4)

        eq7[6].set_color(YELLOW)
        eq7[8].set_color(YELLOW)
        eq7[10].set_color(YELLOW)
        eq7[12].set_color(YELLOW)
        eq7[14].set_color(YELLOW)
        eq7[16].set_color(YELLOW)
        eq7[18].set_color(YELLOW)
        eq7[20].set_color(YELLOW)
        eq7[22].set_color(YELLOW)
        eq7[24].set_color(YELLOW)
        eq7[26].set_color(YELLOW)
        eq7[28].set_color(YELLOW)

        self.wait(4)

        eq8 = MathTex("e^","{ix}","=","1","+",
                      "ix","-",
                      "\\frac{1}{2}","x^2","-i",
                      "\\frac{1}{3!}","x^3","+",
                      "\\frac{1}{4!}","x^4","+i",
                      "\\frac{1}{5!}","x^5","-",
                      "\\frac{1}{6!}","x^6","-i",
                      "\\frac{1}{7!}","x^7","+",
                      "..."
                      )
        eq8.scale(0.7).move_to(eq7, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq7, eq8))

        self.wait(4)

        eq8[4:6].set_color(YELLOW)
        eq8[9:12].set_color(YELLOW)
        eq8[15:18].set_color(YELLOW)
        eq8[21:24].set_color(YELLOW)
        
        self.wait(4)

        eq9 = MathTex("e^","{ix}","=","1",
                      "-","\\frac{1}{2}","x^2",
                      "+","\\frac{1}{4!}","x^4",
                      "-","\\frac{1}{6!}","x^6",
                      "+","...",
                      "+i","x",
                      "-i","\\frac{1}{3!}","x^3",
                      "+i","\\frac{1}{5!}","x^5",
                      "-i","\\frac{1}{7!}","x^7",
                      "+","..."
                      )
        eq9.scale(0.7).move_to(eq8, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq8, eq9))

        self.wait(4)

        eq9[15][1].set_color(YELLOW)
        eq9[17][1].set_color(YELLOW)
        eq9[20][1].set_color(YELLOW)
        eq9[23][1].set_color(YELLOW)

        self.wait(4)

        eq10 = MathTex("e^","{ix}","=","1",
                      "-","\\frac{1}{2}","x^2",
                      "+","\\frac{1}{4!}","x^4",
                      "-","\\frac{1}{6!}","x^6",
                      "+","...","+i\left("
                      "x",
                      "-","\\frac{1}{3!}","x^3",
                      "+","\\frac{1}{5!}","x^5",
                      "-","\\frac{1}{7!}","x^7",
                      "+","...\\right)"
                      )
        eq10.scale(0.7).move_to(eq9, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq9, eq10))

        self.wait(4)

        if lang=="eng":
            eq11 =  MathTex("cos(x)","=","\sum_{n=even}^{\infty}{\\frac{(-1)^\\frac{n}{2}}{n!}x^n}").scale(0.7)
            text_1 = Text("From Taylor series", font_size=24)
        else:
            eq11 =  MathTex("cos(x)","=","\sum_{n=par}^{\infty}{\\frac{(-1)^\\frac{n}{2}}{n!}x^n}").scale(0.7)
            text_1 = Text("Das séries de Taylor", font_size=24)
        eq11.next_to(eq10, DOWN, buff=0.5)
        text_1.next_to(eq11, RIGHT, buff=0.5)

        self.play(Write(eq11), Write(text_1))

        self.wait(4)
        
        self.play(Unwrite(text_1))
        eq11[2].set_color(YELLOW)

        self.wait(4)

        eq12 =  MathTex("cos(x)","=","\\frac{(-1)^\\frac{0}{2}}{0!}","x^0",
                        "+","\\frac{(-1)^\\frac{2}{2}}{2!}","x^2",
                        "+","\\frac{(-1)^\\frac{4}{2}}{4!}","x^4",
                        "+","\\frac{(-1)^\\frac{6}{2}}{6!}","x^6",
                        "+..."
                        )
        eq12.scale(0.7).move_to(eq11)

        self.play(TransformMatchingTex(eq11, eq12))

        self.wait(4)

        eq12[2][4:7].set_color(YELLOW)
        eq12[5][4:7].set_color(YELLOW)
        eq12[8][4:7].set_color(YELLOW)
        eq12[11][4:7].set_color(YELLOW)

        self.wait(4)

        eq13 =  MathTex("cos(x)","=","\\frac{(-1)^0}{0!}","x^0",
                        "+","\\frac{(-1)^1}{2!}","x^2",
                        "+","\\frac{(-1)^2}{4!}","x^4",
                        "+","\\frac{(-1)^3}{6!}","x^6",
                        "+..."
                        )
        eq13.scale(0.7).move_to(eq12, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq12, eq13))

        self.wait(4)

        eq13[2][0:5].set_color(YELLOW)
        eq13[5][0:5].set_color(YELLOW)
        eq13[8][0:5].set_color(YELLOW)
        eq13[11][0:5].set_color(YELLOW)

        self.wait(4)

        eq14 =  MathTex("cos(x)","=","\\frac{1}{0!}","x^0",
                        "+","\\frac{-1}{2!}","x^2",
                        "+","\\frac{1}{4!}","x^4",
                        "+","\\frac{-1}{6!}","x^6",
                        "+..."
                        )
        eq14.scale(0.7).move_to(eq13, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq13, eq14))

        self.wait(4)

        eq14[4].set_color(YELLOW)
        eq14[5][0].set_color(YELLOW)
        eq14[10].set_color(YELLOW)
        eq14[11][0].set_color(YELLOW)

        self.wait(4)

        eq15 =  MathTex("cos(x)","=","\\frac{1}{0!}","x^0",
                        "-","\\frac{1}{2!}","x^2",
                        "+","\\frac{1}{4!}","x^4",
                        "-","\\frac{1}{6!}","x^6",
                        "+..."
                        )
        eq15.scale(0.7).move_to(eq14, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq14, eq15))

        self.wait(4)

        eq15[2:4].set_color(YELLOW)
        eq15[5][2:].set_color(YELLOW)

        self.wait(4)

        eq16 =  MathTex("cos(x)","=","1",
                        "-","\\frac{1}{2}","x^2",
                        "+","\\frac{1}{4!}","x^4",
                        "-","\\frac{1}{6!}","x^6",
                        "+..."
                        )
        eq16.scale(0.7).move_to(eq15, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq15, eq16))

        self.wait(4)

        eq10[3:15].set_color(YELLOW)
        eq16.set_color(YELLOW)

        self.wait(4)

        eq17 = MathTex("e^","{ix}","=","cos(x)",
                      "+i","\left("
                      "x",
                      "-","\\frac{1}{3!}","x^3",
                      "+","\\frac{1}{5!}","x^5",
                      "-","\\frac{1}{7!}","x^7",
                      "+","...\\right)"
                      )
        eq17.scale(0.7).move_to(eq10, aligned_edge=RIGHT)

        self.play(
            eq16.animate.move_to(eq10[3:15]).scale(0),
            TransformMatchingTex(eq10, eq17)
            )

        self.wait(4)
        
        if lang == "eng":
            syn = "sin"
            imp = "odd"
            text_1 = Text("From Taylor series", font_size=24)
        else:
            syn = "sen"
            imp = "\\acute{\imath}mpar"
            text_1 = Text("Das séries de Taylor", font_size=24)

        eq18 =  MathTex(syn,"(x)","=","\sum_{n=",imp,"}^{\infty}{\\frac{(-1)^\\frac{n-1}{2}}{n!}x^n}")
        eq18.next_to(eq17, DOWN, buff=0.5).scale(0.7)
        text_1.next_to(eq18, RIGHT, buff=0.5)

        self.play(Write(eq18), Write(text_1))

        self.wait(4)

        self.play(Unwrite(text_1))
        eq18[3:].set_color(YELLOW)

        self.wait(4)

        eq19 =  MathTex(syn,"(x)","=","\\frac{(-1)^\\frac{1-1}{2}}{1!}","x^1",
                        "+","\\frac{(-1)^\\frac{3-1}{2}}{3!}","x^3",
                        "+","\\frac{(-1)^\\frac{5-1}{2}}{5!}","x^5",
                        "+","\\frac{(-1)^\\frac{7-1}{2}}{7!}","x^7",
                        "+..."
                        )
        eq19.scale(0.7).move_to(eq18)

        self.play(TransformMatchingTex(eq18, eq19))

        self.wait(4)

        eq19[3][4:9].set_color(YELLOW)
        eq19[6][4:9].set_color(YELLOW)
        eq19[9][4:9].set_color(YELLOW)
        eq19[12][4:9].set_color(YELLOW)

        self.wait(4)

        eq20 =  MathTex(syn,"(x)","=","\\frac{(-1)^0}{1!}","x^1",
                        "+","\\frac{(-1)^1}{3!}","x^3",
                        "+","\\frac{(-1)^2}{5!}","x^5",
                        "+","\\frac{(-1)^3}{7!}","x^7",
                        "+..."
                        )
        eq20.scale(0.7).move_to(eq19, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq19, eq20))

        self.wait(4)

        eq20[3][0:5].set_color(YELLOW)
        eq20[6][0:5].set_color(YELLOW)
        eq20[9][0:5].set_color(YELLOW)
        eq20[12][0:5].set_color(YELLOW)

        self.wait(4)

        eq21 =  MathTex(syn,"(x)","=","\\frac{1}{1!}","x^1",
                        "+","\\frac{-1}{3!}","x^3",
                        "+","\\frac{1}{5!}","x^5",
                        "+","\\frac{-1}{7!}","x^7",
                        "+..."
                        )
        eq21.scale(0.7).move_to(eq20, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq20, eq21))

        self.wait(4)

        eq21[5].set_color(YELLOW)
        eq21[6][0].set_color(YELLOW)
        eq21[11].set_color(YELLOW)
        eq21[12][0].set_color(YELLOW)

        self.wait(4)

        eq22 =  MathTex(syn,"(x)","=","\\frac{1}{1!}","x^1",
                        "-","\\frac{1}{3!}","x^3",
                        "+","\\frac{1}{5!}","x^5",
                        "-","\\frac{1}{7!}","x^7",
                        "+..."
                        )
        eq22.scale(0.7).move_to(eq21, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq21, eq22))

        self.wait(4)

        eq22[3:5].set_color(YELLOW)

        self.wait(4)

        eq23 =  MathTex(syn,"(x)","=","x",
                        "-","\\frac{1}{3!}","x^3",
                        "+","\\frac{1}{5!}","x^5",
                        "-","\\frac{1}{7!}","x^7",
                        "+..."
                        )
        eq23.scale(0.7).move_to(eq22, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq22, eq23))

        self.wait(4)

        eq17[5:].set_color(YELLOW)
        eq23.set_color(YELLOW)

        self.wait(4)

        eq24 = MathTex("e^","{ix}","=","cos(x)",
                      "+i",syn,"(x)"
                      )
        eq24.scale(0.7).move_to(eq17, aligned_edge=LEFT)

        self.play(
            eq23.animate.move_to(eq17[5:]).scale(0),
            TransformMatchingTex(eq17, eq24)
        )

        self.wait()

        eq1.set_color(YELLOW)
        eq24.set_color(YELLOW)

        self.play(
            eq24.animate.move_to(ORIGIN).scale(0),
            eq1.animate.move_to(ORIGIN)
        )

        self.wait()

        eq1.set_color(WHITE)

if __name__ == "__main__":

    #language
    lang= 'eng'
    #lang = 'port'

    config.quality = "medium_quality"

    if lang=='eng':
        config.output_file="Euler_formula_derivation.mp4"
    else:
        config.output_file="Deducao_formula_Euler.mp4"
    
    scene = Euler_formula_derivation()
    scene.render()

        

        
    

   