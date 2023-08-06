help_cmd = {
	"help": """	help (command)

The help command can give you an instructive about some of the features of the software, as well as point you to related features that might be useful to know.""",


	"genesis": """	genesis [name]
  
Generates a folder for a templ8 project. It will contain the basic core files needed to make one. Base project files and directiories are renamable. 

See: help core_renaming""",

	"divine": """	divine
	
Generates a website from a project in the output folder. The input must contain markup files, as well as other files that will be copied unprocessed to the output. The markup can be KAMI, Textile or Markdown. Core files are renamable.

See: 
	help core_renaming
	help repl8ce
	help custombase""",

	"radio": """	radio

If all the blog core files aren't set up, it generates the basics required of a textile blog.")
Exports the blog to the output folder.

Core blog files and directories aren't renamable.

See: help core_renaming

A blog requires a few things:

- A baseblog file, to model the article pages, article previews and blog index's repl8ce keys
- A blog directory as input
- An output/blog directory as output for the index
- An output/blog/posts directory as output for the articles

The baseblog is a complex file composed of three simple parts, all separated by a -BEGININDEX- keyword.

The first part of the baseblog is the article page template (from now on PAGE). The PAGEs correspond to specific articles, displaying them in full. It is a page file, so it has its own -BEGINPAGE- keyword. It also contains a ##CONTENT## key to put the content of the markup files.

The second part is the blog preview (from now on PREVIEW), which is the short part of the article that appears in the INDEX.

The blog index (the INDEX) is the part of the blog where all the PREVIEWs appear. The third part of the baseblog are the INDEX's repl8ce keys.

	How A File Is Processed

Each article of the blog in markup format (from now on FILE) is processed separately.

Then, the content of the FILE is put in the PAGE. The FILE's repl8ce keys are applied to this PAGE, meaning that you can do things like:

	PAGETITLE=##ARTICLETITLE##

Where the value of ##ARTICLETITLE## is set by a FILE.

Then, this PAGE's content repl8ce keys are applied to the PREVIEW. This PREVIEW is then put in the INDEX. 

PREVIEWs are added to the INDEX in alphabetical order, not chronological.""",

	"neo": """	neo

Uploads all the output files to neocities.
For it to work, there must be a file named .templ8rc in your user directory.
.templ8rc must contain an API key for your website in this format:

DIRNAME_key=YOUR_API_kEY

Where DIRNAME is the name of the directory where your templ8 project is.""",

	"pandoc": """	pandoc

Downloads and installs pandoc, only necessary if you will use Markdown and don't have pandoc already installed.

It is possible for this command to error and still function properly. I don't know why.

This command only needs to be run once in each user. If you've already used it, chances are you won't ever need to use it anymore.""",

	"core_renaming": """	Core Renaming

Core renaming is a cool functionaility that allows you to rename most of the core directories and files.
It works thanks to the d8y file, which cannot be renamed. It uses the same format as single line repl8ce keys.
These are the core rename keys and the files they map to:\n

	KEY		->   FILE/DIR
	------------>-----------
	replace	->	repl8ce
	output	 ->	 output
	input	  ->	  input
	basehtml   ->   basehtml
	txignore   ->   txignore""",

	"custombase": """	Custom Templates

It's possible to give a specific file a template using the CUSTOMBASE repl8ce key, making its value be the path to the template, from the root of the project.

See: help repl8ce""",

	"repl8ce": """	repl8ce

repl8ce keys are what allows your markup files to change parts of your html template.
In the html template, they look like this:

	##KEYVALUE##

You must set a default value for each key in repl8ce. Otherwise, when a file doesn't set a value for a key, it will error. On a markup file, you can set the values of keys like this:

	KEY1=Value number one
	KEY2=a second value
	KEY3=
	-BEGINFILE-

The -BEGINFILE- keyword is important. It determines where the tags end and the content begins. KEY3's value is an empty string.

You can have multiline values like this:

	;;KEY4
	this
	is
	its
	value
	-BEGINFILE-

All multiline keys must go after every line key. The following is considered to be all part of KEY3.

	;;KEY5
	a
	value KEY6=another value To set the default values of keys on repl8ce, simply use this same notation, without the -BEGINFILE- part. Default values can also be empty strings.

The ##CONTENT## keyword is actually a repl8ce key, it's just that its value is determined by the software and not by the user. Other key like this one is the ##LINK## key, which exists only in blogs. Fun!

You can also have a file called simply 'repl8ce' in a folder of so that all files of that folder have its contents as repl8ce keys. These repl8ce keys are overriden by the files' keys.

When a tag's name starts with MD-, KM- or TX-, templ8 will apply the corresponding markup to the tag before doing the repl8ce operations. The actual key value you should use does not have the prefix, for example, the KM-CAKE key should be put as ##CAKE## in the output file.

See:
	help ifkeys
	help forkeys
	help datekeys""",

	"ifkeys": """	IFKEYs

An IFKEY is a type of key that tells templ8 to remove part of the template if a repl8ce tag is not present. The repl8ce tag can then be used as a repl8ce tag as one would normally do.

An IFKEY starts with the $ IF YOURKEYNAME, replacing YOURKEYNAME with the desired repl8ce key. YOURKEYNAME is the value that will be checked for. An IFKEY ends with the $ END keyword.

If you want something to appear when a tag is undefined or set to an empty string, simply do IF NOT YOURKEYNAME.

If YOURKEYNAME isn't present, or is an empty string, everything between the beginning of the IFKEY and the END will be erased. You can use ##YOURKEY## as normal.

See:
	help repl8ce
	help forkeys""",
	"forkeys": """	FORKEYs

A FORKEY is a type of key that tells templ8 to duplicate part of the template if several variations of a repl8ce tag are present. The repl8ce tags can be used as notmal tags as well.

A FORKEY starts with the $FOR YOURKEYNAME [ITERVAR]$, and ends at the $END$ keyword. When processing a file, it'll check for all the keys starting from YOURKEYNAME0 and adding one to that number until it can't find any more keys. The ITERVAR is an Iteration Variable: a single-letter variable name that you can use inside a forkey to set some part of the file to the current iteration depth. This can be used even inside tags.

Iteration variables allow for better control of nested FORs.

See:
	help repl8ce
	help ifkeys""",
	"datekeys": """	Date Keys

You can use #!DATE!# and #!CDATE!# to ask templ8 to replace some part of a file or a template with the current date or the creation date of the file, respectively.""",

	"forkeys": """  PLUGINS

A PLUGIN is an external script that templ8 can execute in some situations. Currently, a plugin can only be called with $PLUGIN [PLUGNAME]$ and $PL [PLUGNAME]$. The former takes content and must be finished with the $END$ keyword, while the former doesn't, and is simialar to simply using a ##KEY##.

Plugins are loaded from the ~/pl8g/ directory. The structure of a plugin is:
	- PLUGNAME
	|--- main.py

Templ8.py calls the main.py script. The script is provided with the following globals:
	output: Starts as the content of the key (or empty if called with $PL$), and its final state is put in the output file
	filepath: A string with the relative path to the current file
	plugpath: A string with the absolute path to the plugin's main.py
	plugdir: A string with the absolute path to the plugin
	repl8ce: A dictionary with the current repl8ce keys. Modifying them can affect the real keys in the file
""",
}
