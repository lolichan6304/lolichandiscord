import os
import discord

from src.filter_tool import find_url, scan_links

class LoliChan(discord.Client):

    def __init__(self, verbose=False):
        super(LoliChan, self).__init__()
        self.verbose = verbose
        self.forbidden_tags = ["loli", "lolicon", "shotacon", "bestiality", "necrophilia", "cannibalism"]
        self.allowed_roles = ["Admin", "Staff", "Moderator"]

    def admin_command_reader(self, content):
        def filterbot(message):
            def help_(message):
                msg = "**FILTERBOT HELP**\n> Available commands:\n```"
                for k, v in ACCEPTABLE_COMMANDS.items():
                    msg += '{}: Usage - {}\n'.format(k, v['desc'])
                msg += '```'
                return msg

            def not_allowed(message):
                return "**forbidden tags:**  {}".format(", ".join(self.forbidden_tags))

            def add_(message):
                to_add = " ".join(message)
                if to_add not in self.forbidden_tags:
                    self.forbidden_tags.append(to_add.lower())
                return not_allowed(message)

            def remove_(message):
                to_add = " ".join(message)
                while to_add in self.forbidden_tags:
                    self.forbidden_tags.remove(to_add.lower())
                return not_allowed(message)

            ACCEPTABLE_COMMANDS = {
                'help' : {'func': help_, 'desc': ''},
                'not_allowed' : {'func': not_allowed, 'desc': ''},
                'add' : {'func': add_, 'desc': ''},
                'remove' : {'func': remove_, 'desc': ''}
            }

            if len(message) == 0:
                return help_(message)

            cmd = message[0]
            if cmd in ACCEPTABLE_COMMANDS.keys():
                return ACCEPTABLE_COMMANDS[cmd]['func'](message[1:])
            else:
                return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

        def help_(message):
            msg = "**TOOLKIT HELP**\n> Available commands:\n```"
            for k, v in ACCEPTABLE_COMMANDS.items():
                msg += '{}: Usage - {}\n'.format(k, v['desc'])
            msg += '```'
            return msg

        def permission(message):
            def help_(message):
                msg = "**PERMISSION HELP**\n> Available commands:\n```"
                for k, v in ACCEPTABLE_COMMANDS.items():
                    msg += '{}: Usage - {}\n'.format(k, v['desc'])
                msg += '```'
                return msg

            def list_permission(message):
                return "**allowed roles:**  {}".format(", ".join(self.allowed_roles))

            def add_(message):
                to_add = " ".join(message)
                if to_add not in self.allowed_roles:
                    self.allowed_roles.append(to_add)
                return list_permission(message)

            def remove_(message):
                to_add = " ".join(message)
                while to_add in self.allowed_roles:
                    self.allowed_roles.remove(to_add)
                return list_permission(message)

            ACCEPTABLE_COMMANDS = {
                'help' : {'func': help_, 'desc': ''},
                'list_permission' : {'func': list_permission, 'desc': ''},
                'add' : {'func': add_, 'desc': ''},
                'remove' : {'func': remove_, 'desc': ''}
            }

            if len(message) == 0:
                return help_(message)

            cmd = message[0]
            if cmd in ACCEPTABLE_COMMANDS.keys():
                return ACCEPTABLE_COMMANDS[cmd]['func'](message[1:])
            else:
                return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

        ACCEPTABLE_COMMANDS = {
            'help' : {'func': help_, 'desc': ''},
            'filterbot' : {'func': filterbot, 'desc': ''},
            'permissions' : {'func': permission, 'desc': ''}
        }
        
        cmd = content.split(' ')[0]
        if cmd in ACCEPTABLE_COMMANDS.keys():
            return ACCEPTABLE_COMMANDS[cmd]['func'](content.split(' ')[1:])
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
                if role.name in self.allowed_roles and not_found:
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
                await message.channel.send(f"Hi {message.author.mention}, your nhentai link(s) contain(s) the {msg} tag(s), please do not send links with these tag(s)!")
        
            