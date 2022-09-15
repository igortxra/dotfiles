vim.cmd [[
try
  colorscheme catppuccin
    " colorscheme tokyonight
catch /^Vim\%((\a\+)\)\=:E185/
  colorscheme default
  set background=dark
endtry
]]
