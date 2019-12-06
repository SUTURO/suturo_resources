\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{../ti1}[2018/04/28 The format class for the releases of Technische Informatik 1]
\LoadClass[a4paper, 12pt]{scrartcl}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[ngerman]{babel}
\RequirePackage{xcolor}
\RequirePackage[right=2cm,left=2cm,top=2cm,bottom=4cm]{geometry}
\RequirePackage{listings}
\RequirePackage{gensymb}

\newcommand{\authors}[4]{
  \gdef\authori{#1}
  \gdef\authorii{#2}
  \gdef\authoriii{#3}
  \gdef\authoriv{#4}
}

\newcommand{\tutor}[1]{
  \gdef\thetutor{#1}
}

\newcommand{\tutnr}[1]{
  \gdef\thetutnr{#1}
}

\newcommand{\sheet}[1]{
  \gdef\sheetnr{#1}
}

\newcommand{\group}[1]{
  \gdef\groupnr{#1}
}

\newcommand{\room}[1]{
  \gdef\theroom{#1}
}

\newcommand{\fromto}[3]{
  \gdef\tday{#1}
  \gdef\tfrom{#2}
  \gdef\tto{#3}
}

\renewcommand{\maketitle}{
  \fcolorbox{red}{lightgray}{
    \begin{minipage}{16cm}
      \begin{tabular}{p{0.25\textwidth}p{0.25\textwidth}p{0.25\textwidth}p{0.25\textwidth}}
      %\begin{tabular}{c c c c}
        \authori & \authorii & \authoriii & \authoriv
      \end{tabular}
      \hrule
      \vspace{4mm}
      \begin{tabular}{p{0.33\textwidth}p{0.33\textwidth}p{0.33\textwidth}}
      %\begin{tabular}{l c r}
        Tutor: & \LARGE\sffamily Technische & Tutorium: \textcolor{orange}{\thetutnr} \\
        \textcolor{orange}{\thetutor} & \LARGE\sffamily Informatik I & Gruppe: \textcolor{orange}{\groupnr}\\
        \textcolor{blue}{\theroom} & \textcolor{blue}{\tday,} & \textcolor{blue}{\tfrom Uhr - \tto Uhr}
      \end{tabular}
    \end{minipage}
  }
  
  \addvspace{15mm}
  
  \begin{center}
    \LARGE\sffamily \textbf{\"{U}bungsblatt \sheetnr}
  \end{center}
  \begin{center}
    Abgabe: \@date
  \end{center}
}

\renewcommand{\thesection}{
  \fcolorbox{purple}{white}{\color{purple}Aufgabe \arabic{section}}
}

\renewcommand{\thesubsection}{
  \color{lime}\alph{subsection})
}

% fix line numbering for ranges and add space
\makeatletter
\def\lst@MSkipToFirst{%
    \global\advance\lst@lineno\@ne
    \ifnum \lst@lineno=\lst@firstline
        \def\lst@next{\lst@LeaveMode \global\lst@newlines\z@
        \lst@OnceAtEOL \global\let\lst@OnceAtEOL\@empty
        \ifnum \c@lstnumber>0
            \vspace{2 mm}
        \fi
        \lst@InitLstNumber % Added to work with modified \lsthk@PreInit.
        \lsthk@InitVarsBOL
        \c@lstnumber=\numexpr-1+\lst@lineno % this enforces the displayed line numbers to always be the input line numbers
        \lst@BOLGobble}%
        \expandafter\lst@next
    \fi}
\makeatother

\definecolor{sourcecode}{rgb}{1.0, 1.0, 0.88}

\lstset{
  basicstyle=\ttfamily\tiny,
  commentstyle=\color{gray},
  tabsize=4,
  xleftmargin=0.1\textwidth,
  xrightmargin=0.1\textwidth,
  keywordstyle=\textbf,
  breaklines=true,
  captionpos=b,
  numbers=left,
  literate=
  {á}{{\'a}}1 {é}{{\'e}}1 {í}{{\'i}}1 {ó}{{\'o}}1 {ú}{{\'u}}1
  {Á}{{\'A}}1 {É}{{\'E}}1 {Í}{{\'I}}1 {Ó}{{\'O}}1 {Ú}{{\'U}}1
  {à}{{\`a}}1 {è}{{\`e}}1 {ì}{{\`i}}1 {ò}{{\`o}}1 {ù}{{\`u}}1
  {À}{{\`A}}1 {È}{{\'E}}1 {Ì}{{\`I}}1 {Ò}{{\`O}}1 {Ù}{{\`U}}1
  {ä}{{\"a}}1 {ë}{{\"e}}1 {ï}{{\"i}}1 {ö}{{\"o}}1 {ü}{{\"u}}1
  {Ä}{{\"A}}1 {Ë}{{\"E}}1 {Ï}{{\"I}}1 {Ö}{{\"O}}1 {Ü}{{\"U}}1
  {â}{{\^a}}1 {ê}{{\^e}}1 {î}{{\^i}}1 {ô}{{\^o}}1 {û}{{\^u}}1
  {Â}{{\^A}}1 {Ê}{{\^E}}1 {Î}{{\^I}}1 {Ô}{{\^O}}1 {Û}{{\^U}}1
  {œ}{{\oe}}1 {Œ}{{\OE}}1 {æ}{{\ae}}1 {Æ}{{\AE}}1 {ß}{{\ss}}1
  {µ}{{$\mu$}}1 {°}{{\degree}}1,
  backgroundcolor=\color{sourcecode}
}