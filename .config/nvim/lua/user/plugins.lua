local fn = vim.fn

-- Automatically install packer
local install_path = fn.stdpath("data") .. "/site/pack/packer/start/packer.nvim"
if fn.empty(fn.glob(install_path)) > 0 then
	PACKER_BOOTSTRAP = fn.system({
		"git",
		"clone",
		"--depth",
		"1",
		"https://github.com/wbthomason/packer.nvim",
		install_path,
	})
	print("Installing packer close and reopen Neovim...")
	vim.cmd([[packadd packer.nvim]])
end

-- Autocommand that reloads neovim whenever you save the plugins.lua file
vim.cmd([[
  augroup packer_user_config
    autocmd!
    autocmd BufWritePost plugins.lua source <afile> | PackerSync
  augroup end
]])

-- Use a protected call so we don't error out on first use
local status_ok, packer = pcall(require, "packer")
if not status_ok then
	return
end

-- Have packer use a popup window
packer.init({
	display = {
		open_fn = function()
			return require("packer.util").float({ border = "rounded" })
		end,
	},
})

-- Install your plugins here
return packer.startup(function(use)

  -- Super Basics --
	use({ "wbthomason/packer.nvim", commit = "00ec5adef58c5ff9a07f11f45903b9dbbaa1b422" }) -- Have packer manage itself
	use({ "nvim-lua/plenary.nvim", commit = "968a4b9afec0c633bc369662e78f8c5db0eba249" }) -- Useful lua functions used by lots of plugins
	use({ "windwp/nvim-autopairs", commit = "fa6876f832ea1b71801c4e481d8feca9a36215ec" }) -- Autopairs, integrates with both cmp and treesitter
  
  -- Tree --
  use({ "kyazdani42/nvim-web-devicons", commit = "8d2c5337f0a2d0a17de8e751876eeb192b32310e" })
	use({ "kyazdani42/nvim-tree.lua", commit = "bdb6d4a25410da35bbf7ce0dbdaa8d60432bc243" })

  -- Colorschemes --
	use({ "folke/tokyonight.nvim", commit = "8223c970677e4d88c9b6b6d81bda23daf11062bb" })
  use { "catppuccin/nvim", as = "catppuccin" }

  -- Bottom Status Line
  use {
    'nvim-lualine/lualine.nvim',
    requires = { 'kyazdani42/nvim-web-devicons', opt = true }
   }

  -- Top bufferline
  use {'akinsho/bufferline.nvim', tag = "v2.*", requires = 'kyazdani42/nvim-web-devicons'}

  -- Key Helper --
  use "folke/which-key.nvim"

  -- Telescope --
  use { 
    'nvim-telescope/telescope.nvim', 
    tag = '0.1.0', 
    requires = { {'nvim-lua/plenary.nvim'} }
  }
 
  -- Markdown Previewer
  use({ "iamcco/markdown-preview.nvim", run = "cd app && npm install",setup = function() vim.g.mkdp_filetypes = { "markdown" } end, ft = { "markdown" }, })

  -- LSP
  use 'neovim/nvim-lspconfig' -- Configurations for Nvim LSP
  use "williamboman/mason.nvim" -- Package manager for neovim
  use "williamboman/mason-lspconfig.nvim"

  --
	-- Automatically set up your configuration after cloning packer.nvim
	-- Put this at the end after all plugins
	if PACKER_BOOTSTRAP then
		require("packer").sync()
	end
end)
