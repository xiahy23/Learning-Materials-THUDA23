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


\begin{center}
\begin{tabularx}{\columnwidth}{|c|c|X|}
\hline
偶对称 & $a_0=\frac{2}{T_1}\int_0^{\frac{T_1}{2}}f(t)dt$ & $F_n$实偶函数 \\
& $a_n=\frac{4}{T_1}\int_0^{\frac{T_1}{2}}f(t)\cos(n\omega_1t)dt,$ & $\varphi_n : 0/180^\circ$ \\
& $b_n=0$ & \\
\hline
奇对称 & $b_n=\frac{4}{T_1}\int_0^{\frac{T_1}{2}}f(t)\sin(n\omega_1t)dt,$ & $F_n$虚奇函数 \\
& $a_0=a_n=0$ & $\varphi_n :90^\circ/270^\circ$ \\
\hline
奇谐对称 & $a_0=a_{2k}=b_{2k}=0$ & \\
& $a_{2k+1}=\frac{4}{T_1}\int_0^{\frac{T_1}{2}}f(t)\cos((2k+1)\omega_1t)dt$ & \\
& $b_{2k+1}=\frac{4}{T_1}\int_0^{\frac{T_1}{2}}f(t)\sin((2k+1)\omega_1t)dt$ & \\
\hline
\end{tabularx}
\end{center}


一个域的离散化会导致另一个域的周期性，一个域的连续性必然导致另一个域的非周期性。四种类型信号及其傅里叶表示如下：(离散傅里叶级数中 $W=e^{-j\frac{2\pi}{N}}$)

\begin{center}
\begin{tabularx}{\columnwidth}{|p{6pt}|X|X|p{6pt}|}
\hline
时域 & 周期 & 非周期 & \\
\hline
连续 & 傅里叶级数(FS)$x(t)=\sum\limits^{+\infty}_{n=-\infty} X_n e^{jn\Omega_1 t}$；$X(n)=\frac{1}{T_1}\int^{+\frac{T}{2}}_{-\frac{T}{2}} x_t e^{-jn\Omega_1 t}dt$ & 傅里叶变换(FT)$x(t)= \frac{1}{2\pi}\int^{\infty}_{-\infty} X(\Omega) e^{j\Omega t}d\Omega$；$X(\Omega)=\int^{\infty}_{-\infty} x(t) e^{-j\Omega t}dt$ & 非周期\\
\hline
离散 & 离散时间傅里叶级数(DTFS)$IDFS[\widetilde{X}[k]]=\widetilde{x}[n]=\frac{1}{N}\sum\limits^{N-1}_{k=0}\widetilde{X}[k]W^{-nk}$；$DFS[\widetilde{x}[n]]=\widetilde{X}[k]=\sum^{N-1}_{n=0} \widetilde{x}[n] W^{nk}$ & 离散时间傅里叶变换(DTFT)$x[n]=\frac{1}{2\pi}\int^{\pi}_{-\pi}X(e^{j\omega})e^{j\omega n}d\omega$；$X(e^{j\omega})=\sum\limits^{\infty}_{-\infty}x[n]e^{-j\omega n}$ & 周期 \\
\hline
 & 离散 & 连续 & 频域 \\
\hline
\end{tabularx}
\end{center}
