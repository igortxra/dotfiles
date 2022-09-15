local options = {
    number = true,
    relativenumber = true,
    scrolloff = 10,
    colorcolumn = "80",
    signcolumn = "yes",
    cmdheight = 2,
    updatetime = 100,
    encoding = "utf-8",
    timeoutlen = 500,
    autoread = true,
    backup = false,
    writebackup = false,
    splitbelow = true,
    splitright = true,
    tabstop = 2,
    softtabstop = 2,
    shiftwidth = 2,
    smarttab = true,
    expandtab = true,
    hidden = true,
    hlsearch = true,
    incsearch = true,
    ignorecase = true,
    smartcase = true,
    clipboard = "unnamedplus",
    cursorline = true,
    undofile = true,
    swapfile = false,
    wrap = false,
    completeopt = { "menuone", "noselect" }, -- mostly just for cmp
    mouse = "a"
}

-- Set all options
for k, v in pairs(options) do
    vim.opt[k] = v
end

vim.cmd[[
    filetype on
    filetype plugin on
    filetype indent on
]]

