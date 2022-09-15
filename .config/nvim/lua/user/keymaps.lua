local keymap = vim.api.nvim_set_keymap 

local opts = { noremap = true, silent = true }

--Remap space as leader key
keymap("", "<Space>", "<Nop>", opts)
vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Insert Mode --
-- Insert to normal mode
keymap("i", "ii", "<esc>", opts)

-- Normal Mode --
-- Write file
opts["desc"] = "Write"
keymap("n", "<leader>w", ":w<CR>", opts)

-- Close Buffer
opts["desc"] = "Close buffer"
keymap("n", "<leader>q", ":bd<CR>", opts)

-- Quit
opts["desc"] = "Quit"
keymap("n", "<leader>Q", ":q<CR>", opts)

-- File Explorer
opts["desc"] = "Explorer"
keymap("n", "<leader>e", ":NvimTreeToggle<CR>", opts)

-- No highlight
opts["desc"] = "Highlight OFF"
keymap("n", "<leader>h", ":nohl<CR>", opts)

-- Reload config
opts["desc"] = "Reload configurations"
keymap("n", "<leader><leader>r", ":source $MYVIMRC<CR>", opts)

-- Edit config
opts["desc"] = "Edit configurations"
keymap("n", "<leader><leader>e", ":e $MYVIMRC<CR>", opts)

-- Navigate in buffers
opts["desc"] = "Next Buffer"
keymap("n", "<S-l>", ":bnext<CR>", opts)

opts["desc"] = "Previous Buffer"
keymap("n", "<S-h>", ":bprevious<CR>", opts)

-- Change focus
opts["desc"] = nil
keymap("n", "<C-h>", "<C-w>h", opts)
keymap("n", "<C-j>", "<C-w>j", opts)
keymap("n", "<C-k>", "<C-w>k", opts)
keymap("n", "<C-l>", "<C-w>l", opts)
keymap("n", "<C-h>", "<C-w>h", opts)

-- Resize with arrows
opts["desc"] = nil
keymap("n", "<C-Up>", ":resize -2<CR>", opts)
keymap("n", "<C-Down>", ":resize +2<CR>", opts)
keymap("n", "<C-Left>", ":vertical resize -2<CR>", opts)
keymap("n", "<C-Right>", ":vertical resize +2<CR>", opts)

-- Move line up and down
opts["desc"] = nil
keymap("n", "<A-j>", ":m .+1<CR>==", opts)
keymap("n", "<A-k>", ":m .-2<CR>==", opts)

-- New blank lines / new lines in insert mode
opts["desc"] = nil
keymap("n", "oo", "o", opts)
keymap("n", "oO", "O", opts)
keymap("n", "o", "o<esc>k", opts)
keymap("n", "O", "O<esc>j", opts)

-- Telescope
opts["desc"] = "Find Files"
keymap("n", "<leader>ff", ":Telescope find_files<CR>", opts)

opts["desc"] = "Grep"
keymap("n", "<leader>fg", ":Telescope live_grep<CR>", opts)

opts["desc"] = "Buffers"
keymap("n", "<leader>b", "<cmd>lua require('telescope.builtin').buffers(require('telescope.themes').get_dropdown{previewer = false})<cr>", opts)

-- Packer
opts["desc"] = "Packer Install"
keymap("n", "<leader>pi", ":PackerInstall<CR>", opts)

opts["desc"] = "Packer Status"
keymap("n", "<leader>ps", ":PackerStatus<CR>", opts)

opts["desc"] = "Packer Sync"
keymap("n", "<leader>pu", ":PackerSync<CR>", opts)

opts["desc"] = "Packer Clean"
keymap("n", "<leader>pc", ":PackerClean<CR>", opts)

-- Visual --
-- Stay in indent mode
opts["desc"] = nil
keymap("v", "<", "<gv", opts)
keymap("v", ">", ">gv", opts)
