\cancel需要cancel宏包
align环境下看不出里面到底啥有问题，改成equation环境就知道了
&对齐需要amsmath宏包

分栏状态与figure环境不兼容，要自定义
\newenvironment{figurehere}
    {\def\@captype{figure}}
    {}
\makeatother


		
	\textbf{函数相等} $F=G \Leftrightarrow F \subseteq G \land G \subseteq F$，且两函数 $F$ 和 $G$ 相等一定满足：
	
	1. $\text{dom} F = \text{dom} G$
	
	2. $\forall x \in \text{dom} F = \text{dom} G$，都有 $F(x) = G(x)$。


	\textbf{$A_1$ 在 $f$ 下的像、函数的像、完全原像} $f(A_1) = \{ f(x) \mid x \in A_1 \}$，称 $f(A_1)$ 为 $A_1$ 在 $f$ 下的像；$A_1 = A$ 时称 $f(A)$ 为函数的像；称 $f^{-1}(B_1) = \{ x \mid x \in A \land f(x) \in B_1 \}$ 为 $B_1$ 在 $f$ 下的完全原像。注意区分函数的值和像，即 $f(x) \in B, f(A_1) \subseteq B$。一般有 $f^{-1}(f(A_1)) \neq A_1$，但 $A_1 \subseteq f^{-1}(f(A_1))$。


$A$ 的每个子集 $A'$ 对应一个特征函数，可以用特征函数标记 $A$ 的不同子集。