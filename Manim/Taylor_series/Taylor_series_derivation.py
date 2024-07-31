"""
Euler's formula derivation

Author: Marcelo Falcão de Oliveira
Affiliation: University of São Paulo (USP)
             São Carlos School of Engineering (EESC)
             Materials Engineering Department (SMM)
Contact: marcelo.falcao@usp.br

Description:
It produces a mp4 movie explaining the Tayulor's series derivation.

License:
MIT License (https://opensource.org/licenses/MIT)

Purpose:
Educational tool for undergrad students.

Packages needed:
manim
ps.: must have Latex in your system

Usage:
$ Taylor_series_derivation.py

You can choose between english or portuguese (Brazil)
by setting the variable 'lang' in the #Main

Date: July/2024
Version: 1.0
"""

from manim import *

class Taylor_series_derivation(Scene):
    def construct(self):
        
        self.cover()
        self.wait(4)
        
        self.remove(*self.mobjects)
        self.slide_1()
        self.wait(6)

        self.remove(*self.mobjects)
        self.slide_2()
        self.wait(6)
        
        self.remove(*self.mobjects)
        self.slide_3()
        self.wait(6) 
        
        self.remove(*self.mobjects)
        self.slide_4()
        self.wait(6)
               
    def Sin_Taylor(self):

        x_min, x_max = -5,5
        axes = Axes(
            x_range=[x_min, x_max, 1], 
            y_range=[-5, 5, 1],  
            axis_config ={'tip_height':0.2, 'tip_width':0.1},
        )
                    
        grau_1 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t, 0]),
            t_range = [x_min, x_max],
            )
                       
        grau_3 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_5 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_7 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5-1/5040*t**7, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_9 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5-1/5040*t**7+1/362880*t**9, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_11 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5-1/5040*t**7+1/362880*t**9-1/39916800*t**11, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_13 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5-1/5040*t**7+1/362880*t**9-1/39916800*t**11+1/518918400*t**13, 0]),
            t_range = [x_min, x_max],
            )
        
        grau_15 = axes.plot_parametric_curve(
            lambda t: 
            np.array([t, t-1/6*t**3+1/120*t**5-1/5040*t**7+1/362880*t**9-1/39916800*t**11+1/518918400*t**13-1/7783776000*t**15, 0]),
            t_range = [x_min, x_max],
            )
                        
        graf = VGroup(grau_1, grau_3, grau_5, grau_7, grau_9, grau_11, grau_13, grau_15)
                      
        return graf
   
    def cover(self):
        
        self.play(Write(self.Sin_Taylor().shift(DOWN)), run_time=4)

        if lang=="eng":
            title = Text("Taylor series \n"
                         "derivation", font_size=48, line_spacing=1.5)
        else:
            title =  Text("Dedução das \n"
                          "séries de Taylor", font_size=48, line_spacing=1.5)
        title.shift(UP*2)
        self.play(Write(title), run_time=2)
 
    def slide_1(self):

        # padrão
        figurinha = self.Sin_Taylor()
        figurinha.scale(0.08).to_corner(UL, buff=0.2)
        self.add(figurinha)

        # Add the title
        if lang=='eng':
            title = Text("Taylor series", font_size=48)
        else:
            title = Text("Séries de Taylor", font_size=48)
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
            textbox_1 = Tex(r"We want to represent any function \(f(x)\) \\"
                            r"as an infinite sum of polynomial terms.")
        else:
            textbox_1 = Tex(r"Queremos representar qualquer função \(f(x)\) \\"
                            r"por uma somatória infinita de termos polinomiais.")
        textbox_1.next_to(separation_line, DOWN, buff=0.5)

        eq1a = MathTex("f(x)","=","c_0","+","c_1(x-a)","+","c_2(x-a)^2","+")
        eq1b = MathTex("c_3(x-a)^3","+","c_4(x-a)^4","+","...","+","c_n(x-a)^n")
        
        eq2 =  MathTex("n\in\mathbb{N},n\\to\infty")

        eq1a.next_to(textbox_1, DOWN, buff=0.5).shift(LEFT)
        eq1b.next_to(eq1a[2], DOWN, aligned_edge=LEFT, buff=0.2)
        eq2.next_to(eq1b, DOWN, aligned_edge=LEFT, buff=0.5 )
        
        self.play(Write(textbox_1), Write(eq1a), Write(eq1b), Write(eq2))

        self.wait(12)

        self.play(Unwrite(textbox_1), Unwrite(eq2))

        if lang=='eng':
            textbox_1 = Tex(r"Let's set \(x=a\)")
        else:
            textbox_1 = Tex(r"Vamos fazer \(x=a\)")
        textbox_1.next_to(eq1a, UP, buff=0.5)

        self.play(Write(textbox_1))

        self.wait(4)

        textbox_1[0][-3:].set_color(YELLOW)
        eq1a[0][2].set_color(YELLOW)
        eq1a[4][3].set_color(YELLOW)
        eq1a[6][3].set_color(YELLOW)
        eq1b[0][3].set_color(YELLOW)
        eq1b[2][3].set_color(YELLOW)
        eq1b[6][3].set_color(YELLOW)

        self.wait(4)

        eq2a = MathTex("f(a)","=","c_0","+","c_1(a-a)","+","c_2(a-a)^2","+").move_to(eq1a, aligned_edge=LEFT)
        eq2b = MathTex("c_3(a-a)^3","+","c_4(a-a)^4","+","...","+","c_n(a-a)^n").move_to(eq1b, aligned_edge=LEFT)
        
        self.play(
            textbox_1[0][10:].copy().animate.move_to( eq1a[0][2]).scale(0),
            textbox_1[0][10:].copy().animate.move_to( eq1a[4][3]).scale(0),
            textbox_1[0][10:].copy().animate.move_to( eq1a[6][3]).scale(0),
            textbox_1[0][10:].copy().animate.move_to( eq1b[0][3]).scale(0),
            textbox_1[0][10:].copy().animate.move_to( eq1b[2][3]).scale(0),
            textbox_1[0][10:].copy().animate.move_to( eq1b[6][3]).scale(0),
            FadeOut(textbox_1),
            TransformMatchingTex(eq1a, eq2a),
            TransformMatchingTex(eq1b, eq2b),
            run_time=2
        )

        self.wait(4)

        eq2a[4][3:6].set_color(YELLOW)
        eq2a[6][3:6].set_color(YELLOW)
        eq2b[0][3:6].set_color(YELLOW)
        eq2b[2][3:6].set_color(YELLOW)
        eq2b[6][3:6].set_color(YELLOW)

        self.wait(4)

        eq3a = MathTex("f(a)","=","c_0","+","c_1(0)","+","c_2(0)^2","+").move_to(eq2a, aligned_edge=LEFT)
        eq3b = MathTex("c_3(0)^3","+","c_4(0)^4","+","...","+","c_n(0)^n").move_to(eq2b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq2a, eq3a), TransformMatchingTex(eq2b, eq3b))

        self.wait(4)

        eq3a[3:].set_color( YELLOW)
        eq3b.set_color(YELLOW)

        self.wait(4)

        eq4 = MathTex("f(a)","=","c_0").move_to(eq3a, aligned_edge=LEFT)

        self.play(FadeOut(eq3b), TransformMatchingTex(eq3a, eq4))

        self.wait(4)

        eq5 = MathTex("c_0","=","f(a)").move_to(eq4, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4, eq5))

        self.wait(4)
           
        self.play(eq5.animate.scale(0.8).next_to(figurinha, DOWN, aligned_edge=LEFT, buff=0.5))

        const_0 = eq5

        self.wait()

        if lang=='eng':
            textbox_1 = Tex(r"Now, let's calculate the \\"
                            r"first derivative of \(f(x)\).")
        else:
            textbox_1 = Tex(r"Vamos agora calcular a \\"
                            r"primeira derivada de \(f(x)\).")
            
        textbox_1.next_to(separation_line, DOWN, buff=0.5)

        eq1a = MathTex("f(x)","=","c_0","+","c_1(x-a)","+","c_2(x-a)^2","+")
        eq1b = MathTex("c_3(x-a)^3","+","c_4(x-a)^4","+","...","+","c_n(x-a)^n")

        eq1a.next_to(textbox_1, DOWN, buff=0.5).shift(LEFT)
        eq1b.next_to(eq1a[2], DOWN, aligned_edge=LEFT, buff=0.2)
               
        self.play(Write(textbox_1), Write(eq1a), Write(eq1b))

        self.wait(6)

        eq2a = MathTex("f'(x)","=","c_1","+","2c_2(x-a)","+","3c_3(x-a)^2","+").move_to(eq1a, aligned_edge=LEFT)
        eq2b = MathTex("4c_4(x-a)^3","+","...","+","nc_n(x-a)^{n-1}").move_to(eq1b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq1a, eq2a), TransformMatchingTex(eq1b, eq2b))

        self.wait(4)

        if lang=='eng':
            textbox_2 = Tex(r"Let's set \(x=a\)")
        else:
            textbox_2 = Tex(r"Vamos fazer \(x=a\)")
        textbox_2.move_to(textbox_1)

        self.play(ReplacementTransform(textbox_1, textbox_2))

        self.wait(4)

        textbox_2[0][-3:].set_color(YELLOW)
        eq2a[0][3].set_color(YELLOW)
        eq2a[4][4].set_color(YELLOW)
        eq2a[6][4].set_color(YELLOW)
        eq2b[0][4].set_color(YELLOW)
        eq2b[4][4].set_color(YELLOW)
        
        self.wait(4)

        eq3a = MathTex("f'(a)","=","c_1","+","2c_2(a-a)","+","3c_3(a-a)^2+").move_to(eq2a, aligned_edge=LEFT)
        eq3b = MathTex("4c_4(a-a)^3","+","...","+","nc_n(a-a)^{n-1}").move_to(eq2b, aligned_edge=LEFT)

        self.play(
            textbox_2[0][10:].copy().animate.move_to( eq2a[0][3]).scale(0),
            textbox_2[0][10:].copy().animate.move_to( eq2a[4][4]).scale(0),
            textbox_2[0][10:].copy().animate.move_to( eq2a[6][4]).scale(0),
            textbox_2[0][10:].copy().animate.move_to( eq2b[0][4]).scale(0),
            textbox_2[0][10:].copy().animate.move_to( eq2b[4][4]).scale(0),
            FadeOut(textbox_2),
            TransformMatchingTex(eq2a, eq3a),
            TransformMatchingTex(eq2b, eq3b),
            run_time=2
        )

        self.wait(4)

        eq3a[4][4:7].set_color(YELLOW)
        eq3a[6][4:7].set_color(YELLOW)
        eq3b[0][4:7].set_color(YELLOW)
        eq3b[4][4:7].set_color(YELLOW)

        self.wait(4)

        eq4a = MathTex("f'(a)","=","c_1","+","2c_2(0)","+","3c_3(0)^2","+").move_to(eq3a, aligned_edge=LEFT)
        eq4b = MathTex("4c_4(0)^3","+","...","+","nc_n(0)^{n-1}").move_to(eq3b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq3a, eq4a), TransformMatchingTex(eq3b, eq4b))

        self.wait(4)

        eq4a[3:].set_color(YELLOW)
        eq4b.set_color(YELLOW)

        self.wait(4)

        eq5 = MathTex("f'(a)","=","c_1").move_to(eq4a, aligned_edge=LEFT)
        self.play(FadeOut(eq4b), TransformMatchingTex(eq4a, eq5))

        self.wait(4)

        eq6 = MathTex("c_1","=","f'(a)").move_to(eq5, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5, eq6))

        self.wait(4)

        self.play(eq6.animate.scale(0.8).next_to(const_0, DOWN, aligned_edge=LEFT))

        const_1 = eq6

        self.wait()

        if lang=='eng':
            textbox_1 = Tex(r"Let's continue the process for \\"
                            r"the higher derivatives up to \(n\).")
        else:
            textbox_1 = Tex(r"Vamos continuar o processo para \\"
                            r"as derivadas superiores até \(n\).")
        textbox_1.next_to(separation_line, DOWN, buff=0.5)

        eq2a = MathTex("f'(x)","=","c_1","+","2c_2(x-a)","+","3c_3(x-a)^2","+")
        eq2b = MathTex("4c_4(x-a)^3","+","...","+","nc_n(x-a)^{n-1}").next_to(eq2a[2], DOWN, aligned_edge=LEFT)

        self.play(Write(textbox_1), Write(eq2a), Write(eq2b))

        self.wait(4)

        eq3a = MathTex("f''(x)","=","2c_2","+","3.2c_3(x-a)","+").move_to(eq2a, aligned_edge=LEFT)
        eq3b = MathTex("4.3c_4(x-a)^2","+","...","+","n(n-1)c_n(x-a)^{n-2}").move_to(eq2b, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq2a, eq3a), TransformMatchingTex(eq2b, eq3b), FadeOut(textbox_1))

        self.wait(4)

        eq1 = MathTex("x=a").next_to(eq3a, UP, buff=0.5)

        self.play(Write(eq1))
        
        self.wait(4)

        eq1.set_color(YELLOW)
        eq3a[0][4].set_color(YELLOW)
        eq3a[4][6].set_color(YELLOW)
        eq3b[0][6].set_color(YELLOW)
        eq3b[4][9].set_color(YELLOW)

        self.wait(4)

        eq4a = MathTex("f''(a)","=","2c_2","+","3.2c_3(a-a)","+").move_to(eq3a, aligned_edge=LEFT)
        eq4b = MathTex("4.3c_4(a-a)^2","+","...","+","n(n-1)c_n(a-a)^{n-2}").move_to(eq3b, aligned_edge=LEFT)

        self.play(
            eq1.animate.move_to( eq3a[0][4]).scale(0),
            eq1.copy().animate.move_to( eq3a[4][6]).scale(0),
            eq1.copy().animate.move_to( eq3b[0][6]).scale(0),
            eq1.copy().animate.move_to( eq3b[4][9]).scale(0),
            TransformMatchingTex(eq3a, eq4a),
            TransformMatchingTex(eq3b, eq4b),
            run_time=2
        )

        self.wait(4)

        eq4a[4][6:9].set_color(YELLOW)
        eq4b[0][6:9].set_color(YELLOW)
        eq4b[4][9:12].set_color(YELLOW)

        self.wait(4)

        eq5a = MathTex("f''(a)","=","2c_2","+","3.2c_3(0)+").move_to(eq4a, aligned_edge=LEFT)
        eq5b = MathTex("4.3c_4(0)^2","+","...","+","n(n-1)c_n(0)^{n-2}").move_to(eq4b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4a, eq5a), TransformMatchingTex(eq4b, eq5b))

        self.wait(4)

        eq5a[3:].set_color(YELLOW)
        eq5b.set_color(YELLOW)

        self.wait(4)

        eq6 = MathTex("f''(a)","=","2c_2").move_to(eq5a, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5a, eq6), FadeOut(eq5b))

        self.wait(4)

        eq7 = MathTex("c_2","=","\\frac{f''(a)}{2}").move_to(eq6, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq6, eq7))

        self.wait(4)

        self.play(eq7.animate.scale(0.8).next_to(const_1, DOWN, aligned_edge=LEFT))

        const_2 = eq7

        self.wait(4)

        eq2a = MathTex("f''(x)","=","2c_2","+","3.2c_3(x-a)","+").next_to(const_2, RIGHT, buff=0.5)
        eq2b = MathTex("4.3c_4(x-a)^2","+","...","+","n(n-1)c_n(x-a)^{n-2}").next_to(eq2a[2], DOWN, aligned_edge=LEFT)

        self.play(Write(eq2a), Write(eq2b))

        self.wait(4)

        eq3a = MathTex("f'''(x)","=","3.2c_3","+","4.3.2c_4(x-a)").move_to(eq2a, aligned_edge=LEFT)
        eq3b = MathTex("+","...","+","n(n-1)(n-2)c_n(x-a)^{n-3}").move_to(eq2b, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq2a, eq3a), TransformMatchingTex(eq2b, eq3b))

        self.wait(4)

        eq1 = MathTex("x=a").next_to(eq3a, UP, buff=0.5)

        self.play(Write(eq1))
        
        self.wait(4)

        eq1.set_color(YELLOW)
        eq3a[0][5].set_color(YELLOW)
        eq3a[4][8].set_color(YELLOW)
        eq3b[3][14].set_color(YELLOW)

        self.wait(4)
        
        eq4a = MathTex("f'''(a)","=","3.2c_3","+","4.3.2c_4(a-a)").move_to(eq3a, aligned_edge=LEFT)
        eq4b = MathTex("+","...","+","n(n-1)(n-2)c_n(a-a)^{n-3}").move_to(eq3b, aligned_edge=LEFT)

        self.play(
            eq1.animate.move_to( eq3a[0][5]).scale(0),
            eq1.copy().animate.move_to( eq3a[4][8]).scale(0),
            eq1.copy().animate.move_to( eq3b[3][14]).scale(0),
            TransformMatchingTex(eq3a, eq4a),
            TransformMatchingTex(eq3b, eq4b),
            run_time=2
        )

        self.wait(4)

        eq4a[4][8:11].set_color(YELLOW)
        eq4b[3][14:17].set_color(YELLOW)

        self.wait(4)

        eq5a = MathTex("f'''(a)","=","3.2c_3","+","4.3.2c_4(0)").move_to(eq4a, aligned_edge=LEFT)
        eq5b = MathTex("+","...","+","n(n-1)(n-2)c_n(0)^{n-3}").move_to(eq4b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4a, eq5a), TransformMatchingTex(eq4b, eq5b))

        self.wait(4)

        eq5a[3:].set_color(YELLOW)
        eq5b.set_color(YELLOW)

        self.wait(4)

        eq6 = MathTex("f'''(a)","=","3.2c_3").move_to(eq5a, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5a, eq6), FadeOut(eq5b))

        self.wait(4)

        eq7 = MathTex("c_3","=","\\frac{f'''(a)}{3.2}").move_to(eq6, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq6, eq7))

        self.wait(4)

        self.play(eq7.animate.scale(0.8).next_to(const_2, DOWN, aligned_edge=LEFT))

        const_3 = eq7

        self.wait(4)

        dots = Text(".\n.\n.").scale(0.7).next_to(const_3, DOWN)

        self.play(Write(dots), run_time=3)
     
        self.wait(4)

        eq2a = MathTex("f'''(x)","=","3.2c_3","+","4.3.2c_4(x-a)").next_to(const_2, RIGHT, buff=0.5)
        eq2b = MathTex("+","...","+","n(n-1)(n-2)c_n(x-a)^{n-3}").next_to(eq2a[2], DOWN, aligned_edge=LEFT)

        self.play(Write(eq2a), Write(eq2b))

        self.wait(4)

        eq3a = MathTex("f^n{'}(x)","=","n(n-1)(n-2)","...").move_to(eq2a, aligned_edge=LEFT)
        eq3b = MathTex("...","(n-(n-2))(n-(n-1)).c_n(x-a)^{n-n}").move_to(eq2b, aligned_edge=LEFT)
                
        self.play(Write(eq3a), FadeOut(eq2a), run_time=2)
        self.wait()
        self.play(Write(eq3b), FadeOut(eq2b), run_time=2)

        self.wait(4)

        eq3b[1][26:].set_color(YELLOW)

        self.wait(4)

        eq4b = MathTex("...","(n-(n-2))(n-(n-1)).c_n(x-a)^0").move_to(eq3b, aligned_edge=LEFT)
               
        self.play(TransformMatchingTex(eq3b, eq4b))

        self.wait(4)

        eq4b[1][21:].set_color(YELLOW)

        self.wait(4)

        eq5b = MathTex("...","(n-(n-2))(n-(n-1)).c_n").move_to(eq4b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4b, eq5b))

        self.wait(4)

        eq5b[1][0:19].set_color(YELLOW)

        self.wait(4)

        eq6b = MathTex("...","2.1.c_n").move_to(eq5b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5b, eq6b))

        self.wait(4)

        eq7 = MathTex("f^n{'}(x)","=","n(n-1)(n-2)...2.1.c_n").move_to(eq3a, aligned_edge=LEFT)

        self.play(FadeOut(eq6b), TransformMatchingTex(eq3a, eq7))

        self.wait(4)

        eq8 =  MathTex("n!=n(n-1)(n-2)...2.1").next_to(eq7, DOWN, buff=0.5)

        self.play(Write(eq8))

        self.wait(4)

        eq8.set_color(YELLOW)
        eq7[2][0:18].set_color(YELLOW)

        self.wait(4)

        eq9 = MathTex("f^n{'}(x)","=","n!c_n").move_to(eq7, aligned_edge=RIGHT)

        self.play(
            eq8.animate.move_to(eq7[2][0:18]).scale(0),
            TransformMatchingTex(eq7, eq9)
        )

        self.wait(4)

        eq1 = MathTex("x=a").next_to(eq9, UP, buff=0.5)

        self.play(Write(eq1))
        
        self.wait(4)

        eq1.set_color(YELLOW)
        eq9[0][4].set_color(YELLOW)

        self.wait(4)

        eq10 = MathTex("f^n{'}(a)","=","n!c_n").move_to(eq9, aligned_edge=LEFT)

        self.play(
            eq1.animate.move_to(eq9[0][4]).scale(0),
            TransformMatchingTex(eq9, eq10)
            )

        self.wait(4)

        eq11 = MathTex("c_n","=","\\frac{f^n{'}(a)}{n!}").move_to(eq10, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq10, eq11))

        self.wait(4)

        self.play(eq11.animate.scale(0.8).next_to(dots, DOWN))

        const_n = eq11

        self.wait(4)
        
        if lang=='eng':
            textbox_1 = Tex(r"Let's substitute all the \\"
                            r"constants in \(f(x)\).")
        else:
            textbox_1 = Tex(r"Vamos substituir todas as \\"
                            r"constantes em \(f(x)\).")

        textbox_1.next_to(separation_line, DOWN, buff=0.5)

        eq1a = MathTex("f(x)","=","c_0","+","c_1(x-a)","+","c_2(x-a)^2+")
        eq1b = MathTex("c_3(x-a)^3","+","c_4(x-a)^4","+","...","+","c_n(x-a)^n")

        eq1a.next_to(textbox_1, DOWN, buff=0.5)
        eq1b.next_to(eq1a[2], DOWN, aligned_edge=LEFT, buff=0.2)
               
        self.play(Write(textbox_1), Write(eq1a), Write(eq1b))

        self.wait(6)

        const_0.set_color(YELLOW)
        const_1.set_color(YELLOW)
        const_2.set_color(YELLOW)
        const_3.set_color(YELLOW)
        dots.set_color(YELLOW)
        const_n.set_color(YELLOW)

        eq1a[2].set_color(YELLOW)
        eq1a[4][0:2].set_color(YELLOW)
        eq1a[6][0:2].set_color(YELLOW)
        eq1b[0][0:2].set_color(YELLOW)
        eq1b[2][0:2].set_color(YELLOW)
        eq1b[6][0:2].set_color(YELLOW)

        self.wait(4)

        eq2a = MathTex("f(x)","=","f(a)","+","f'(a)(x-a)","+","\\frac{f''(a)}{2}(x-a)^2","+").to_edge(LEFT, buff=0.5)
        eq2b = MathTex("\\frac{f'''(a)}{3.2}(x-a)^3","+","\\frac{f''''(a)}{4.3.2}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n").next_to(eq2a[2], DOWN, aligned_edge=LEFT, buff=0.5)

        self.play(
            const_0.animate.move_to(eq1a[2]).scale(0),
            const_1.animate.move_to(eq1a[4][0:2]).scale(0),
            const_2.animate.move_to(eq1a[6][0:2]).scale(0),
            const_3.animate.move_to(eq1b[0][0:2]).scale(0),
            dots.animate.move_to(eq1b[4]).rotate(PI/2).scale(0),
            const_n.animate.move_to(eq1b[6][0:2]).scale(0),
            TransformMatchingTex(eq1a, eq2a),
            TransformMatchingTex(eq1b, eq2b)
        )

        self.play(Unwrite(textbox_1))

        self.wait(4)

        eq2a[2].set_color(YELLOW)
        eq2a[4][0:5].set_color(YELLOW)

        self.wait(4)

        eq3a = MathTex("f(x)","=","\\frac{f(a)}{1}","+","\\frac{f'(a)}{1}(x-a)","+","\\frac{f''(a)}{2}(x-a)^2","+").move_to(eq2a, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq2a, eq3a))

        self.wait(4)
        
        eq3a[2][0].set_color(YELLOW)
        eq3a[4][0:2].set_color(YELLOW)
        eq3a[6][0:3].set_color(YELLOW)
        eq2b[0][0:4].set_color(YELLOW)
        eq2b[2][0:5].set_color(YELLOW)

        self.wait(4)

        eq4a = MathTex("f(x)","=","\\frac{f^0{'}(a)}{1}","+","\\frac{f^1{'}(a)}{1}(x-a)","+","\\frac{f^2{'}(a)}{2}(x-a)^2","+").move_to(eq3a, aligned_edge=LEFT)
        eq4b = MathTex("\\frac{f^3{'}(a)}{3.2}(x-a)^3","+","\\frac{f^4{'}(a)}{4.3.2}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n").move_to(eq2b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq3a, eq4a), TransformMatchingTex(eq2b, eq4b))

        self.wait(4)

        eq4a[2].set_color(YELLOW)
        eq4a[4][8:].set_color(YELLOW)

        self.wait(4)

        eq5a = MathTex("f(x)","=","\\frac{f^0{'}(a)}{1}(x-a)^0","+","\\frac{f^1{'}(a)}{1}(x-a)^1","+","\\frac{f^2{'}(a)}{2}(x-a)^2","+").move_to(eq4a, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq4a, eq5a))

        self.wait(4)

        eq5a[2][7].set_color(YELLOW)
        eq5a[4][7].set_color(YELLOW)
        eq5a[6][7].set_color(YELLOW)
        eq4b[0][7:10].set_color(YELLOW)
        eq4b[2][7:12].set_color(YELLOW)

        self.wait(4)

        eq6a = MathTex("f(x)","=","\\frac{f^0{'}(a)}{0!}(x-a)^0","+","\\frac{f^1{'}(a)}{1!}(x-a)^1","+","\\frac{f^2{'}(a)}{2!}(x-a)^2","+").move_to(eq5a, aligned_edge=LEFT)
        eq6b = MathTex("\\frac{f^3{'}(a)}{3!}(x-a)^3","+","\\frac{f^4{'}(a)}{4!}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n").move_to(eq4b, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq5a, eq6a), TransformMatchingTex(eq4b, eq6b))

        self.wait(4)

        eq7 = MathTex("f(x)","=","\sum_{n=0}^{\infty}{\\frac{f^n{'}(a)}{n!}(x-a)^n}").move_to(eq6a, aligned_edge=LEFT)
        
        copia = eq6b[6].copy().set_color(YELLOW)
        self.add(copia)

        self.wait(4)
        
        self.play(
            copia.animate.move_to(eq7[2][5:]),
            TransformMatchingTex(eq6a, eq7),
            FadeOut(eq6b)
        )
        self.remove(copia)

        self.wait(2)

        self.play(eq7.animate.move_to(ORIGIN))

        if lang=='eng':
            textbox_1 = Text("General formula.", font_size=24)
        else:
            textbox_1 = Tex("Fórmula geral.", font_size=24)
        textbox_1.next_to(eq7, UP, buff=0.5)

        self.play(Write(textbox_1))
       
    def slide_2(self):

        # padrão
        figurinha = self.Sin_Taylor()
        figurinha.scale(0.08).to_corner(UL, buff=0.2)
        self.add(figurinha)

        # Add the title
        if lang=='eng':
            title = Text("The exponential function", font_size=48)
        else:
            title = Text("A função exponencial", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        eq1 = MathTex("f(x)","=","\sum_{n=0}^{\infty}{\\frac{f^n{'}(a)}{n!}(x-a)^n}")
        
        self.play(Write(eq1))

        eq2 = MathTex("f(x)","=","\\frac{f(a)}{0!}(x-a)^0","+","\\frac{f'(a)}{1!}(x-a)^1","+","\\frac{f''(a)}{2!}(x-a)^2","+")
        eq3 = MathTex("\\frac{f'''(a)}{3!}(x-a)^3","+","\\frac{f''''(a)}{4!}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n")

        self.play(eq1.animate.to_edge(LEFT))
        eq2.move_to(eq1, aligned_edge=LEFT)
        eq3.next_to(eq2[2], DOWN, aligned_edge=LEFT, buff=0.5)

        self.wait(2)

        self.play(FadeOut(eq1), Write(eq2))
        self.play(Write(eq3))
                
        self.wait(4)

        eq={}

        eq[4] = MathTex("f(x)=e^x").next_to(eq2[2], UP, buff=1, aligned_edge=LEFT)
        eq[5] = MathTex("f(a)=e^a").next_to(eq[4], RIGHT)
        eq[6] = MathTex("f'(a)=e^a").next_to(eq[5], RIGHT)
        eq[7] = MathTex("f''(a)=e^a").next_to(eq[6], RIGHT)
        eq[8] = MathTex("f'''(a)=e^a").next_to(eq3, DOWN, buff=1, aligned_edge=LEFT)
        eq[9] = MathTex("f''''(a)=e^a").next_to(eq[8], RIGHT)
        eq[10] = MathTex("...").next_to(eq[9], RIGHT)
        eq[11] = MathTex("f^n{'}(a)=e^a").next_to(eq[10], RIGHT)

        for i in eq.keys():
            self.play(Write(eq[i]))

        self.wait(4)
        
        for i in range(4,12):
            eq[i].set_color(YELLOW)
        
        eq2[0].set_color(YELLOW)
        eq2[2][0:4].set_color(YELLOW)
        eq2[4][0:5].set_color(YELLOW)
        eq2[6][0:6].set_color(YELLOW)
        eq3[0][0:7].set_color(YELLOW)
        eq3[2][0:8].set_color(YELLOW)
        eq3[6][0:6].set_color(YELLOW)

        self.wait(4)

        eq12 = MathTex("e^x","=","\\frac{e^a}{0!}(x-a)^0","+","\\frac{e^a}{1!}(x-a)^1","+","\\frac{e^a}{2!}(x-a)^2","+").move_to(eq2, aligned_edge=LEFT)
        eq13 = MathTex("\\frac{e^a}{3!}(x-a)^3","+","\\frac{e^a}{4!}(x-a)^4","+","...","+","\\frac{e^a}{n!}(x-a)^n").move_to(eq3, aligned_edge=LEFT)

        self.play(
            eq[4].animate.move_to(eq2[0]).scale(0),
            eq[5].animate.move_to(eq2[2][0:4]).scale(0),
            eq[6].animate.move_to(eq2[4][0:5]).scale(0),
            eq[7].animate.move_to(eq2[6][0:6]).scale(0),
            eq[8].animate.move_to(eq3[0][0:7]).scale(0),
            eq[9].animate.move_to(eq3[2][0:8]).scale(0),
            eq[10].animate.move_to(eq3[4]).scale(0),
            eq[11].animate.move_to(eq3[6][0:6]).scale(0),
            TransformMatchingTex(eq2, eq12),
            TransformMatchingTex(eq3, eq13)
        )

        self.wait(4)

        eq14 =  MathTex("a=0").next_to(eq12, UP, buff=1)

        self.play(Write(eq14))

        self.wait(4)

        eq14.set_color(YELLOW)

        eq12[2][1].set_color(YELLOW)
        eq12[2][8].set_color(YELLOW)
        eq12[4][1].set_color(YELLOW)
        eq12[4][8].set_color(YELLOW)
        eq12[6][1].set_color(YELLOW)
        eq12[6][8].set_color(YELLOW)
        eq13[0][1].set_color(YELLOW)
        eq13[0][8].set_color(YELLOW)
        eq13[2][1].set_color(YELLOW)
        eq13[2][8].set_color(YELLOW)
        eq13[6][1].set_color(YELLOW)
        eq13[6][8].set_color(YELLOW)

        self.wait(4)

        eq15 = MathTex("e^x","=","\\frac{e^0}{0!}(x-0)^0","+","\\frac{e^0}{1!}(x-0)^1","+","\\frac{e^0}{2!}(x-0)^2","+").move_to(eq12, aligned_edge=LEFT)
        eq16 = MathTex("\\frac{e^0}{3!}(x-0)^3","+","\\frac{e^0}{4!}(x-0)^4","+","...","+","\\frac{e^0}{n!}(x-0)^n").move_to(eq13, aligned_edge=LEFT)

        self.play(
            eq14.animate.move_to(eq12[2][1]).scale(0),
            eq14.copy().animate.move_to(eq12[2][8]).scale(0),
            eq14.copy().animate.move_to(eq12[4][1]).scale(0),
            eq14.copy().animate.move_to(eq12[4][8]).scale(0),
            eq14.copy().animate.move_to(eq12[6][1]).scale(0),
            eq14.copy().animate.move_to(eq12[6][8]).scale(0),
            eq14.copy().animate.move_to(eq13[0][1]).scale(0),
            eq14.copy().animate.move_to(eq13[0][8]).scale(0),
            eq14.copy().animate.move_to(eq13[2][1]).scale(0),
            eq14.copy().animate.move_to(eq13[2][8]).scale(0),
            eq14.copy().animate.move_to(eq13[6][1]).scale(0),
            eq14.copy().animate.move_to(eq13[6][8]).scale(0),
            TransformMatchingTex(eq12, eq15),
            TransformMatchingTex(eq13, eq16)
        )

        self.wait(4)

        eq15[2][0:2].set_color(YELLOW)
        eq15[2][5:10].set_color(YELLOW)
        eq15[4][0:2].set_color(YELLOW)
        eq15[4][5:10].set_color(YELLOW)
        eq15[6][0:2].set_color(YELLOW)
        eq15[6][5:10].set_color(YELLOW)
        eq16[0][0:2].set_color(YELLOW)
        eq16[0][5:10].set_color(YELLOW)
        eq16[2][0:2].set_color(YELLOW)
        eq16[2][5:10].set_color(YELLOW)
        eq16[6][0:2].set_color(YELLOW)
        eq16[6][5:10].set_color(YELLOW)

        self.wait(4)

        eq17 = MathTex("e^x","=","\\frac{1}{0!}x^0","+","\\frac{1}{1!}x^1","+","\\frac{1}{2!}x^2","+").move_to(eq15, aligned_edge=LEFT)
        eq18 = MathTex("\\frac{1}{3!}x^3","+","\\frac{1}{4!}x^4","+","...","+","\\frac{1}{n!}x^n").move_to(eq16, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq15, eq17), TransformMatchingTex(eq16, eq18))

        self.wait(4)

        eq19 = MathTex("e^x","=","\sum_{n=0}^{\infty}","{\\frac{1}{n!}x^n}").move_to(eq17, aligned_edge=LEFT)

        copia = eq18[-1].copy().set_color(YELLOW)
        self.add(copia)

        self.wait(4)

        self.play(
            copia.animate.move_to(eq19[3]),
            TransformMatchingTex(eq17, eq19),
            FadeOut(eq18)
        )
        self.remove(copia)

        self.wait(2)

        self.play(eq19.animate.move_to(ORIGIN))

        self.wait(4)

        eq20 = MathTex("e^x=1+x+\\frac{1}{2!}x^2+\\frac{1}{3!}x^3+\\frac{1}{4!}x^4+...").next_to(eq19, DOWN, buff=1)

        self.play(Write(eq20))

    def slide_3(self):

        # padrão
        figurinha = self.Sin_Taylor()
        figurinha.scale(0.08).to_corner(UL, buff=0.2)
        self.add(figurinha)

        # Add the title
        if lang=='eng':
            title = Text("The sine function", font_size=48)
        else:
            title = Text("A função seno", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        separation_line = Line(
            start=title.get_corner(DOWN + LEFT) + 0.2*DOWN,
            end=title.get_corner(DOWN + RIGHT) + 0.2*DOWN,
            color=BLUE_D
        )
        self.play(Create(separation_line))

        eq1 = MathTex("f(x)","=","\sum_{n=0}^{\infty}{\\frac{f^n{'}(a)}{n!}(x-a)^n}")
        
        self.play(Write(eq1))

        eq2 = MathTex("f(x)","=","\\frac{f(a)}{0!}(x-a)^0","+","\\frac{f'(a)}{1!}(x-a)^1","+","\\frac{f''(a)}{2!}(x-a)^2","+")
        eq3 = MathTex("\\frac{f'''(a)}{3!}(x-a)^3","+","\\frac{f''''(a)}{4!}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n")

        self.play(eq1.animate.to_edge(LEFT))
        eq2.move_to(eq1, aligned_edge=LEFT)
        eq3.next_to(eq2[2], DOWN, aligned_edge=LEFT, buff=0.5)

        self.wait(2)

        self.play(FadeOut(eq1), Write(eq2))
        self.play(Write(eq3))
                
        self.wait(4)

        eq={}

        if lang=='eng':
            eq[4] = MathTex("f(x)=sin(x)").next_to(eq2, UP, buff=1, aligned_edge=LEFT)
            eq[5] = MathTex("f(a)=sin(a)").next_to(eq[4], RIGHT)
            eq[6] = MathTex("f'(a)=cos(a)").next_to(eq[5], RIGHT)
            eq[7] = MathTex("f''(a)=-sin(a)").next_to(eq[6], RIGHT)
            eq[8] = MathTex("f'''(a)=-cos(a)").next_to(eq3, DOWN, buff=1, aligned_edge=LEFT)
            eq[9] = MathTex("f''''(a)=sin(a)").next_to(eq[8], RIGHT)
            eq[10] = MathTex("......").next_to(eq[9], RIGHT)
        else:
            eq[4] = MathTex("f(x)=sen(x)").next_to(eq2, UP, buff=1, aligned_edge=LEFT)
            eq[5] = MathTex("f(a)=sen(a)").next_to(eq[4], RIGHT)
            eq[6] = MathTex("f'(a)=cos(a)").next_to(eq[5], RIGHT)
            eq[7] = MathTex("f''(a)=-sen(a)").next_to(eq[6], RIGHT)
            eq[8] = MathTex("f'''(a)=-cos(a)").next_to(eq3, DOWN, buff=1, aligned_edge=LEFT)
            eq[9] = MathTex("f''''(a)=sen(a)").next_to(eq[8], RIGHT)
            eq[10] = MathTex("......").next_to(eq[9], RIGHT)
            
        for i in eq.keys():
            self.play(Write(eq[i]))

        self.wait(4)
        
        for i in eq.keys():
            eq[i].set_color(YELLOW)
        
        eq2[0].set_color(YELLOW)
        eq2[2][0:4].set_color(YELLOW)
        eq2[4][0:5].set_color(YELLOW)
        eq2[6][0:6].set_color(YELLOW)
        eq3[0][0:7].set_color(YELLOW)
        eq3[2][0:8].set_color(YELLOW)
        eq3[6][0:6].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
            eq12 = MathTex("sin(x)","=","\\frac{sin(a)}{0!}(x-a)^0","+","\\frac{cos(a)}{1!}(x-a)^1","+","\\frac{-sin(a)}{2!}(x-a)^2").move_to(eq2, aligned_edge=LEFT)
            eq13 = MathTex("+","\\frac{-cos(a)}{3!}(x-a)^3","+","\\frac{sin(a)}{4!}(x-a)^4","+","......").move_to(eq3, aligned_edge=LEFT)
        else:
            eq12 = MathTex("sen(x)","=","\\frac{sen(a)}{0!}(x-a)^0","+","\\frac{cos(a)}{1!}(x-a)^1","+","\\frac{-sen(a)}{2!}(x-a)^2").move_to(eq2, aligned_edge=LEFT)
            eq13 = MathTex("+","\\frac{-cos(a)}{3!}(x-a)^3","+","\\frac{sen(a)}{4!}(x-a)^4","+","......").move_to(eq3, aligned_edge=LEFT)

        self.play(
            eq[4].animate.move_to(eq2[0]).scale(0),
            eq[5].animate.move_to(eq2[2][0:4]).scale(0),
            eq[6].animate.move_to(eq2[4][0:5]).scale(0),
            eq[7].animate.move_to(eq2[6][0:6]).scale(0),
            eq[8].animate.move_to(eq3[0][0:7]).scale(0),
            eq[9].animate.move_to(eq3[2][0:8]).scale(0),
            eq[10].animate.move_to(eq3[4]).scale(0),
            TransformMatchingTex(eq2, eq12),
            TransformMatchingTex(eq3, eq13)
        )

        eq14 =  MathTex("a=0").next_to(eq12, UP, buff=1)

        self.play(Write(eq14))

        self.wait(4)

        eq14.set_color(YELLOW)

        eq12[2][4].set_color(YELLOW)
        eq12[2][12].set_color(YELLOW)
        eq12[4][4].set_color(YELLOW)
        eq12[4][12].set_color(YELLOW)
        eq12[6][5].set_color(YELLOW)
        eq12[6][13].set_color(YELLOW)
        eq13[1][5].set_color(YELLOW)
        eq13[1][13].set_color(YELLOW)
        eq13[3][4].set_color(YELLOW)
        eq13[3][12].set_color(YELLOW)
        
        self.wait(4)

        if lang=="eng":
            eq15 = MathTex("sin(x)","=","\\frac{sin(0)}{0!}(x-0)^0","+","\\frac{cos(0)}{1!}(x-0)^1","+","\\frac{-sin(a)}{2!}(x-a)^2").move_to(eq12, aligned_edge=LEFT)
            eq16 = MathTex("+","\\frac{-cos(0)}{3!}(x-0)^3","+","\\frac{sin(0)}{4!}(x-0)^4","+","......").move_to(eq13, aligned_edge=LEFT)
        else:
            eq15 = MathTex("sen(x)","=","\\frac{sen(0)}{0!}(x-0)^0","+","\\frac{cos(0)}{1!}(x-0)^1","+","\\frac{-sen(a)}{2!}(x-a)^2").move_to(eq12, aligned_edge=LEFT)
            eq16 = MathTex("+","\\frac{-cos(0)}{3!}(x-0)^3","+","\\frac{sen(0)}{4!}(x-0)^4","+","......").move_to(eq13, aligned_edge=LEFT)

        self.play(
            eq14.animate.move_to(eq12[2][4]).scale(0),
            eq14.copy().animate.move_to(eq12[2][12]).scale(0),
            eq14.copy().animate.move_to(eq12[4][4]).scale(0),
            eq14.copy().animate.move_to(eq12[4][12]).scale(0),
            eq14.copy().animate.move_to(eq12[6][5]).scale(0),
            eq14.copy().animate.move_to(eq12[6][13]).scale(0),
            eq14.copy().animate.move_to(eq13[1][5]).scale(0),
            eq14.copy().animate.move_to(eq13[1][13]).scale(0),
            eq14.copy().animate.move_to(eq13[3][4]).scale(0),
            eq14.copy().animate.move_to(eq13[3][12]).scale(0),
            TransformMatchingTex(eq12, eq15),
            TransformMatchingTex(eq13, eq16)
        )

        self.wait(4)

        eq15[2][0:6].set_color(YELLOW)
        eq15[2][9:14].set_color(YELLOW)
        eq15[4][0:6].set_color(YELLOW)
        eq15[4][9:14].set_color(YELLOW)
        eq15[6][1:7].set_color(YELLOW)
        eq15[6][10:15].set_color(YELLOW)
        eq16[1][1:7].set_color(YELLOW)
        eq16[1][10:15].set_color(YELLOW)
        eq16[3][0:6].set_color(YELLOW)
        eq16[3][9:14].set_color(YELLOW)
        
        self.wait(4)

        if lang=="eng":
            eq17 = MathTex("sin(x)","=","\\frac{0}{0!}x^0","+","\\frac{1}{1!}x^1","+","\\frac{-0}{2!}x^2").move_to(eq15, aligned_edge=LEFT)
        else:
            eq17 = MathTex("sen(x)","=","\\frac{0}{0!}x^0","+","\\frac{1}{1!}x^1","+","\\frac{-0}{2!}x^2").move_to(eq15, aligned_edge=LEFT)
        eq18 = MathTex("+","\\frac{-1}{3!}x^3","+","\\frac{0}{4!}x^4","+","......").move_to(eq16, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq15, eq17), TransformMatchingTex(eq16, eq18))

        self.wait(4)

        eq17[2].set_color(YELLOW)
        eq17[6].set_color(YELLOW)
        eq18[3].set_color(YELLOW)

        self.wait(2)

        if lang=="eng":
            eq19 = MathTex("sin(x)","=","\\frac{1}{1!}x^1","+").move_to(eq17, aligned_edge=LEFT)
        else:
            eq19 = MathTex("sen(x)","=","\\frac{1}{1!}x^1","+").move_to(eq17, aligned_edge=LEFT)
        eq20 = MathTex("+","\\frac{-1}{3!}x^3","+","......").move_to(eq18, aligned_edge=LEFT)

        self.play(
            eq17[2].animate.scale(0),
            eq17[6].animate.scale(0),
            eq18[3].animate.scale(0)
        )

        self.wait()

        self.play(
            TransformMatchingTex(eq17, eq19),
            TransformMatchingTex(eq18, eq20)
        )

        self.wait()

        if lang=="eng":
            eq21 = MathTex("sin(x)","=","\\frac{1}{1!}x^1","+","\\frac{-1}{3!}x^3","+","......").move_to(eq19, aligned_edge=LEFT)
        else:
            eq21 = MathTex("sen(x)","=","\\frac{1}{1!}x^1","+","\\frac{-1}{3!}x^3","+","......").move_to(eq19, aligned_edge=LEFT)

        self.play(
            TransformMatchingTex(eq19, eq21),
            FadeOut(eq20)
        )

        self.wait(4)

        if lang=="eng":
            eq22 = MathTex("sin(x)","=","\\frac{1}{1!}x^1","+","\\frac{-1}{3!}x^3","+","\\frac{1}{5!}x^5","+","\\frac{-1}{7!}x^7","+","......").move_to(eq21, aligned_edge=LEFT)
        else:
            eq22 = MathTex("sen(x)","=","\\frac{1}{1!}x^1","+","\\frac{-1}{3!}x^3","+","\\frac{1}{5!}x^5","+","\\frac{-1}{7!}x^7","+","......").move_to(eq21, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq21, eq22))

        self.wait(4)

        eq22[2][0].set_color(YELLOW)
        eq22[4][0:2].set_color(YELLOW)
        eq22[6][0].set_color(YELLOW)
        eq22[8][0:2].set_color(YELLOW)
        
        self.wait(4)

        if lang=="eng":
            eq23 = MathTex("sin(x)","=","\\frac{(-1)^0}{1!}x^1","+","\\frac{(-1)^1}{3!}x^3","+","\\frac{(-1)^2}{5!}x^5","+","\\frac{(-1)^3}{7!}x^7","+","......").move_to(eq21, aligned_edge=LEFT)
        else:
            eq23 = MathTex("sen(x)","=","\\frac{(-1)^0}{1!}x^1","+","\\frac{(-1)^1}{3!}x^3","+","\\frac{(-1)^2}{5!}x^5","+","\\frac{(-1)^3}{7!}x^7","+","......").move_to(eq21, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq22, eq23))

        self.wait(4)

        for i in (2,4,6,8):
            eq23[i][4].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
           eq24 = MathTex("sin(x)","=","\\frac{(-1)^{\\frac{1-1}{2}}}{1!}x^1","+","\\frac{(-1)^{\\frac{3-1}{2}}}{3!}x^3","+","\\frac{(-1)^{\\frac{5-1}{2}}}{5!}x^5","+","\\frac{(-1)^{\\frac{7-1}{2}}}{7!}x^7","+","...").move_to(eq23, aligned_edge=LEFT)
        else:
           eq24 = MathTex("sen(x)","=","\\frac{(-1)^{\\frac{1-1}{2}}}{1!}x^1","+","\\frac{(-1)^{\\frac{3-1}{2}}}{3!}x^3","+","\\frac{(-1)^{\\frac{5-1}{2}}}{5!}x^5","+","\\frac{(-1)^{\\frac{7-1}{2}}}{7!}x^7","+","...").move_to(eq23, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq23, eq24))

        eq24.scale(0.9).shift(LEFT)

        self.wait(4)

        eq24[8].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
           eq25 = MathTex("sin(x)","=","\\frac{(-1)^{\\frac{1-1}{2}}}{1!}x^1","+","\\frac{(-1)^{\\frac{3-1}{2}}}{3!}x^3","+","\\frac{(-1)^{\\frac{5-1}{2}}}{5!}x^5","+","...","+","\\frac{(-1)^{\\frac{n-1}{2}}}{n!}x^n")
        else:
           eq25 = MathTex("sen(x)","=","\\frac{(-1)^{\\frac{1-1}{2}}}{1!}x^1","+","\\frac{(-1)^{\\frac{3-1}{2}}}{3!}x^3","+","\\frac{(-1)^{\\frac{5-1}{2}}}{5!}x^5","+","...","+","\\frac{(-1)^{\\frac{n-1}{2}}}{n!}x^n")

        eq25.scale(0.9).move_to(eq23, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq24, eq25))

        self.wait(4)

        eq25[-1].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
           eq26 = MathTex("sin(x)","=","\sum_{n=odd}^{\infty}","{\\frac{(-1)^{\\frac{n-1}{2}}}{n!}x^n}").move_to(eq25, aligned_edge=LEFT)
        else:
           eq26 = MathTex("sen(x)","=","\sum_{n=\\acute{\imath}mpar}^{\infty}","{\\frac{(-1)^{\\frac{n-1}{2}}}{n!}x^n}").move_to(eq25, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq25, eq26))

        self.wait(2)

        self.play(eq26.animate.move_to(ORIGIN))

        self.wait(4)

        if lang=="eng":
            eq27 = MathTex("sin(x)=x-\\frac{1}{3!}x^3+\\frac{1}{5!}x^5-\\frac{1}{7!}x^7+...").next_to(eq26, DOWN, buff=1)
        else:
            eq27 = MathTex("sen(x)=x-\\frac{1}{3!}x^3+\\frac{1}{5!}x^5-\\frac{1}{7!}x^7+...").next_to(eq26, DOWN, buff=1)

        self.play(Write(eq27))

    def slide_4(self):

        # padrão
        figurinha = self.Sin_Taylor()
        figurinha.scale(0.08).to_corner(UL, buff=0.2)
        self.add(figurinha)

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

        eq1 = MathTex("f(x)","=","\sum_{n=0}^{\infty}{\\frac{f^n{'}(a)}{n!}(x-a)^n}")
        
        self.play(Write(eq1))

        eq2 = MathTex("f(x)","=","\\frac{f(a)}{0!}(x-a)^0","+","\\frac{f'(a)}{1!}(x-a)^1","+","\\frac{f''(a)}{2!}(x-a)^2","+")
        eq3 = MathTex("\\frac{f'''(a)}{3!}(x-a)^3","+","\\frac{f''''(a)}{4!}(x-a)^4","+","...","+","\\frac{f^n{'}(a)}{n!}(x-a)^n")

        self.play(eq1.animate.to_edge(LEFT))
        eq2.move_to(eq1, aligned_edge=LEFT)
        eq3.next_to(eq2[2], DOWN, aligned_edge=LEFT, buff=0.5)

        self.wait(2)

        self.play(FadeOut(eq1), Write(eq2))
        self.play(Write(eq3))
                
        self.wait(4)

        eq={}

        if lang=='eng':
            eq[4] = MathTex("f(x)=cos(x)").next_to(eq2, UP, buff=1, aligned_edge=LEFT)
            eq[5] = MathTex("f(a)=cos(a)").next_to(eq[4], RIGHT)
            eq[6] = MathTex("f'(a)=-sin(a)").next_to(eq[5], RIGHT)
            eq[7] = MathTex("f''(a)=-cos(a)").next_to(eq[6], RIGHT)
            eq[8] = MathTex("f'''(a)=sin(a)").next_to(eq3, DOWN, buff=1, aligned_edge=LEFT)
            eq[9] = MathTex("f''''(a)=cos(a)").next_to(eq[8], RIGHT)
            eq[10] = MathTex("......").next_to(eq[9], RIGHT)
        else:
            eq[4] = MathTex("f(x)=cos(x)").next_to(eq2, UP, buff=1, aligned_edge=LEFT)
            eq[5] = MathTex("f(a)=cos(a)").next_to(eq[4], RIGHT)
            eq[6] = MathTex("f'(a)=-sen(a)").next_to(eq[5], RIGHT)
            eq[7] = MathTex("f''(a)=-cos(a)").next_to(eq[6], RIGHT)
            eq[8] = MathTex("f'''(a)=sen(a)").next_to(eq3, DOWN, buff=1, aligned_edge=LEFT)
            eq[9] = MathTex("f''''(a)=cos(a)").next_to(eq[8], RIGHT)
            eq[10] = MathTex("......").next_to(eq[9], RIGHT)
            
        for i in eq.keys():
            self.play(Write(eq[i]))

        self.wait(4)
        
        for i in eq.keys():
            eq[i].set_color(YELLOW)
        
        eq2[0].set_color(YELLOW)
        eq2[2][0:4].set_color(YELLOW)
        eq2[4][0:5].set_color(YELLOW)
        eq2[6][0:6].set_color(YELLOW)
        eq3[0][0:7].set_color(YELLOW)
        eq3[2][0:8].set_color(YELLOW)
        eq3[6][0:6].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
            eq12 = MathTex("cos(x)","=","\\frac{cos(a)}{0!}(x-a)^0","+","\\frac{-sin(a)}{1!}(x-a)^1","+","\\frac{-cos(a)}{2!}(x-a)^2").move_to(eq2, aligned_edge=LEFT)
            eq13 = MathTex("+","\\frac{sin(a)}{3!}(x-a)^3","+","\\frac{cos(a)}{4!}(x-a)^4","+","......").move_to(eq3, aligned_edge=LEFT)
        else:
            eq12 = MathTex("cos(x)","=","\\frac{cos(a)}{0!}(x-a)^0","+","\\frac{-sen(a)}{1!}(x-a)^1","+","\\frac{-cos(a)}{2!}(x-a)^2").move_to(eq2, aligned_edge=LEFT)
            eq13 = MathTex("+","\\frac{sen(a)}{3!}(x-a)^3","+","\\frac{cos(a)}{4!}(x-a)^4","+","......").move_to(eq3, aligned_edge=LEFT)

        self.play(
            eq[4].animate.move_to(eq2[0]).scale(0),
            eq[5].animate.move_to(eq2[2][0:4]).scale(0),
            eq[6].animate.move_to(eq2[4][0:5]).scale(0),
            eq[7].animate.move_to(eq2[6][0:6]).scale(0),
            eq[8].animate.move_to(eq3[0][0:7]).scale(0),
            eq[9].animate.move_to(eq3[2][0:8]).scale(0),
            eq[10].animate.move_to(eq3[4]).scale(0),
            TransformMatchingTex(eq2, eq12),
            TransformMatchingTex(eq3, eq13)
        )

        eq14 =  MathTex("a=0").next_to(eq12, UP, buff=1)

        self.play(Write(eq14))

        self.wait(4)

        eq14.set_color(YELLOW)

        eq12[2][4].set_color(YELLOW)
        eq12[2][12].set_color(YELLOW)
        eq12[4][5].set_color(YELLOW)
        eq12[4][13].set_color(YELLOW)
        eq12[6][5].set_color(YELLOW)
        eq12[6][13].set_color(YELLOW)
        eq13[1][4].set_color(YELLOW)
        eq13[1][12].set_color(YELLOW)
        eq13[3][4].set_color(YELLOW)
        eq13[3][12].set_color(YELLOW)
        
        self.wait(4)

        if lang=="eng":
            eq15 = MathTex("cos(x)","=","\\frac{cos(0)}{0!}(x-0)^0","+","\\frac{-sin(0)}{1!}(x-0)^1","+","\\frac{-cos(a)}{2!}(x-a)^2").move_to(eq12, aligned_edge=LEFT)
            eq16 = MathTex("+","\\frac{sin(0)}{3!}(x-0)^3","+","\\frac{cos(0)}{4!}(x-0)^4","+","......").move_to(eq13, aligned_edge=LEFT)
        else:
            eq15 = MathTex("cos(x)","=","\\frac{cos(0)}{0!}(x-0)^0","+","\\frac{-sen(0)}{1!}(x-0)^1","+","\\frac{-cos(a)}{2!}(x-a)^2").move_to(eq12, aligned_edge=LEFT)
            eq16 = MathTex("+","\\frac{sen(0)}{3!}(x-0)^3","+","\\frac{cos(0)}{4!}(x-0)^4","+","......").move_to(eq13, aligned_edge=LEFT)

        self.play(
            eq14.animate.move_to(eq12[2][4]).scale(0),
            eq14.copy().animate.move_to(eq12[2][12]).scale(0),
            eq14.copy().animate.move_to(eq12[4][5]).scale(0),
            eq14.copy().animate.move_to(eq12[4][13]).scale(0),
            eq14.copy().animate.move_to(eq12[6][5]).scale(0),
            eq14.copy().animate.move_to(eq12[6][13]).scale(0),
            eq14.copy().animate.move_to(eq13[1][4]).scale(0),
            eq14.copy().animate.move_to(eq13[1][12]).scale(0),
            eq14.copy().animate.move_to(eq13[3][4]).scale(0),
            eq14.copy().animate.move_to(eq13[3][12]).scale(0),
            TransformMatchingTex(eq12, eq15),
            TransformMatchingTex(eq13, eq16)
        )

        self.wait(4)

        eq15[2][0:6].set_color(YELLOW)
        eq15[2][9:14].set_color(YELLOW)
        eq15[4][1:7].set_color(YELLOW)
        eq15[4][10:15].set_color(YELLOW)
        eq15[6][1:7].set_color(YELLOW)
        eq15[6][10:15].set_color(YELLOW)
        eq16[1][0:6].set_color(YELLOW)
        eq16[1][9:14].set_color(YELLOW)
        eq16[3][0:6].set_color(YELLOW)
        eq16[3][9:14].set_color(YELLOW)
        
        self.wait(4)

        eq17 = MathTex("cos(x)","=","\\frac{1}{0!}x^0","+","\\frac{-0}{1!}x^1","+","\\frac{-1}{2!}x^2").move_to(eq15, aligned_edge=LEFT)
        eq18 = MathTex("+","\\frac{0}{3!}x^3","+","\\frac{1}{4!}x^4","+","......").move_to(eq16, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq15, eq17), TransformMatchingTex(eq16, eq18))

        self.wait(4)

        eq17[4].set_color(YELLOW)
        eq18[1].set_color(YELLOW)

        self.wait(2)

        eq19 = MathTex("cos(x)","=","\\frac{1}{0!}x^0","+","\\frac{-1}{2!}x^2").move_to(eq17, aligned_edge=LEFT)
        eq20 = MathTex("+","\\frac{1}{4!}x^4","+","......").move_to(eq18, aligned_edge=LEFT)
        
        self.play(
            eq17[4].animate.scale(0),
            eq18[1].animate.scale(0)
        )

        self.wait()

        self.play(
            TransformMatchingTex(eq17, eq19),
            TransformMatchingTex(eq18, eq20)
        )

        self.wait()

        eq21 = MathTex("cos(x)","=","\\frac{1}{0!}x^0","+","\\frac{-1}{2!}x^2","+","\\frac{1}{4!}x^4","+","......").move_to(eq19, aligned_edge=LEFT)
        
        self.play(
            TransformMatchingTex(eq19, eq21),
            FadeOut(eq20)
        )

        self.wait(4)

        eq22 = MathTex("cos(x)","=","\\frac{1}{0!}x^0","+","\\frac{-1}{2!}x^2","+","\\frac{1}{4!}x^4","+","\\frac{-1}{6!}x^6","+","......").move_to(eq21, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq21, eq22))

        self.wait(4)

        eq22[2][0].set_color(YELLOW)
        eq22[4][0:2].set_color(YELLOW)
        eq22[6][0].set_color(YELLOW)
        eq22[8][0:2].set_color(YELLOW)
        
        self.wait(4)

        eq23 = MathTex("cos(x)","=","\\frac{(-1)^0}{0!}x^0","+","\\frac{(-1)^1}{2!}x^2","+","\\frac{(-1)^2}{4!}x^4","+","\\frac{(-1)^3}{6!}x^6","+","......").move_to(eq21, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq22, eq23))

        self.wait(4)

        for i in (2,4,6,8):
            eq23[i][4].set_color(YELLOW)

        self.wait(4)

        eq24 = MathTex("cos(x)","=","\\frac{(-1)^{\\frac{0}{2}}}{0!}x^0","+","\\frac{(-1)^{\\frac{2}{2}}}{2!}x^2","+","\\frac{(-1)^{\\frac{4}{2}}}{4!}x^4","+","\\frac{(-1)^{\\frac{6}{2}}}{6!}x^6","+","...").move_to(eq23, aligned_edge=LEFT)
       
        self.play(TransformMatchingTex(eq23, eq24))

        self.wait(4)

        eq24[8].set_color(YELLOW)

        self.wait(4)

        eq25 = MathTex("cos(x)","=","\\frac{(-1)^{\\frac{0}{2}}}{0!}x^0","+","\\frac{(-1)^{\\frac{2}{2}}}{2!}x^2","+","\\frac{(-1)^{\\frac{4}{2}}}{4!}x^4","+","...","+","\\frac{(-1)^{\\frac{n}{2}}}{n!}x^n").move_to(eq24, aligned_edge=LEFT)
        
        self.play(TransformMatchingTex(eq24, eq25))

        self.wait(4)

        eq25[-1].set_color(YELLOW)

        self.wait(4)

        if lang=="eng":
           eq26 = MathTex("cos(x)","=","\sum_{n=even}^{\infty}","{\\frac{(-1)^{\\frac{n}{2}}}{n!}x^n}").move_to(eq25, aligned_edge=LEFT)
        else:
           eq26 = MathTex("cos(x)","=","\sum_{n=par}^{\infty}","{\\frac{(-1)^{\\frac{n}{2}}}{n!}x^n}").move_to(eq25, aligned_edge=LEFT)

        self.play(TransformMatchingTex(eq25, eq26))

        self.wait(2)

        self.play(eq26.animate.move_to(ORIGIN))

        self.wait(4)

        eq27 = MathTex("cos(x)=1-\\frac{1}{2}x^2+\\frac{1}{4!}x^4-\\frac{1}{6!}x^6+...").next_to(eq26, DOWN, buff=1)

        self.play(Write(eq27))
          
if __name__ == "__main__":

    #language
    lang= 'eng'
    #lang = 'port'

    #config.frame_size = [850,480]
    #config.frame_rate = 15
    config.quality = "medium_quality"

    if lang=='eng':
        config.output_file="Taylor_series_derivation.mp4"
    else:
        config.output_file="Deducao_series_Taylor.mp4"
    
    scene = Taylor_series_derivation()
    scene.render()

        

        
    

   