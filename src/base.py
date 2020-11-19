import discord

from src.filter_tool import find_url, scan_links

class LoliChan(discord.Client):

    def __init__(self, verbose=False):
        super(LoliChan, self).__init__()
        self.verbose = verbose
        self.forbidden_tags = ["loli", "lolicon", "shotacon"]
        self.allowed_roles = ["Admin"]

    def admin_command_reader(self, content):
        def filterbot(message):
            def help_(message):
                return "**FILTERBOT HELP**\n> Available commands:\n```{}```".format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

            def not_allowed(message):
                return "**forbidden tags:**  {}".format(", ".join(self.forbidden_tags))

            def add_(message):
                for i in message:
                    if i.lower() not in self.forbidden_tags:
                        self.forbidden_tags.append(i.lower())
                return not_allowed(message)

            def remove_(message):
                for i in message:
                    while i.lower() in self.forbidden_tags:
                        self.forbidden_tags.remove(i.lower())
                return not_allowed(message)

            ACCEPTABLE_COMMANDS = {
                'help' : help_,
                'not_allowed' : not_allowed,
                'add' : add_,
                'remove' : remove_
            }

            if len(message) == 0:
                return help_(message)

            cmd = message[0]
            if cmd in ACCEPTABLE_COMMANDS.keys():
                return ACCEPTABLE_COMMANDS[cmd](message[1:])
            else:
                return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

        def help_(message):
            return "**TOOLKIT HELP**\n> Available commands:\n```{}```".format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))
        
        ACCEPTABLE_COMMANDS = {
            'help' : help_,
            'filterbot' : filterbot,
        }
        
        cmd = content.split(' ')[0]
        if cmd in ACCEPTABLE_COMMANDS.keys():
            return ACCEPTABLE_COMMANDS[cmd](content.split(' ')[1:])
        else:
            return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

    # initialization
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message):
        ### implement checks
        # prevent recursive case
        if message.author == self.user:
            return

        # command central
        cmd_tag = '!'
        if message.content[:len(cmd_tag)] == cmd_tag:
            not_found = True
            for role in message.author.roles:
                if role.name in self.allowed_roles:
                    reply = self.admin_command_reader(message.content[len(cmd_tag):])
                    await message.channel.send(reply)
                    not_found = False
            if not_found:
                await message.channel.send(f"Hi {message.author.mention}, you do not have the required permission to use this command!")
            
        # filter nhentai tags
        urls = find_url(message.content)
        if len(urls) > 0:
            if self.verbose:
                print('found nhentai links', urls)
            # check to see if message contains bad content
            to_pass, problems = scan_links(urls, self.forbidden_tags)

            # format problems
            if len(problems) == 1:
                msg = problems[0]
            elif len(problems) > 1:
                msg = ", ".join(problems[:-1]) + " and " + problems[-1]

            if to_pass:
                if self.verbose:
                    print('a problemmatic tag was found')
                await message.delete()
                await message.channel.send(f"Hi {message.author.mention}, your nhentai link(s) contains the {msg} tags, please do not send links with these tags!")
        
            