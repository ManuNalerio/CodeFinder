ttk::style theme create azure -parent clam -settings {
    ttk::style configure "." -background "#F0F0F0" -foreground "#000000"
    ttk::style configure "TLabel" -background "#F0F0F0" -foreground "#000000"
    ttk::style configure "TButton" -background "#0078D7" -foreground "#FFFFFF" -padding 6 -relief flat
    ttk::style map "TButton" -background [list active "#005A9E" disabled "#A6A6A6"]
    ttk::style configure "TEntry" -fieldbackground "#FFFFFF" -foreground "#000000"
    ttk::style configure "TCombobox" -fieldbackground "#FFFFFF" -foreground "#000000"
    ttk::style configure "TMenubutton" -background "#0078D7" -foreground "#FFFFFF"
    ttk::style configure "TNotebook" -background "#F0F0F0"
    ttk::style configure "TNotebook.Tab" -background "#D0D0D0" -foreground "#000000"
    ttk::style map "TNotebook.Tab" -background [list selected "#0078D7" active "#005A9E"]
    ttk::style configure "TFrame" -background "#F0F0F0"
}
