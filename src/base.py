import os
import json
import discord

from src.filter_tool import find_url, scan_links

class LoliChan(discord.Client):

    def __init__(self, verbose=False):
        super(LoliChan, self).__init__()
        self.verbose = verbose
        with open('./data/defaults.json') as json_file:
            data = json.load(json_file)
            self.forbidden_tags = data["forbidden_tags"]
            self.allowed_roles = data["allowed_roles"]
            self.admin_cmd_tag = data["admin_cmd_tag"]
            self.cmd_tag = data["cmd_tag"]

    def admin_command_reader(self, content):
        def filterbot(message):
            def help_(message):
                msg = "**FILTERBOT HELP**\n> Available commands:\n```"
                padding = max(list(map(lambda x: len(x), list(ACCEPTABLE_COMMANDS.keys()))))+1
                for k, v in ACCEPTABLE_COMMANDS.items():
                    msg += '{message: <{padding}}| Usage - {description}\n'.format(message=k, padding=padding, description=v['desc'])
                msg += '```'
                return msg

            def not_allowed(message):
                msg = '**Forbidden Tags**\n```'
                padding = max(list(map(lambda x: len(x), list(self.forbidden_tags.keys()))))+1
                for k, v in self.forbidden_tags.items():
                    msg += '{message: <{padding}}| {values}\n'.format(message=k, padding=padding, values=", ".join(sorted(v)))
                msg += '```'
                return msg

            def add_(message):
                channel = message[0]
                to_add = " ".join(message[1:])
                if channel not in self.forbidden_tags.keys():
                    self.forbidden_tags[channel] = [to_add.lower()]
                else:
                    self.forbidden_tags[channel].append(to_add.lower())
                return not_allowed(message)

            def remove_(message):
                channel = message[0]
                to_add = " ".join(message[1:])
                if channel in self.forbidden_tags.keys():
                    while to_add in self.forbidden_tags[channel]:
                        self.forbidden_tags[channel].remove(to_add.lower())
                return not_allowed(message)

            ACCEPTABLE_COMMANDS = {
                'help' : {'func': help_, 'desc': self.admin_cmd_tag+'filterbot help'},
                'list' : {'func': not_allowed, 'desc': self.admin_cmd_tag+'filterbot list'},
                'add' : {'func': add_, 'desc': self.admin_cmd_tag+'filterbot add channel tag [for global tags, use all for channel]'},
                'remove' : {'func': remove_, 'desc': self.admin_cmd_tag+'filterbot remove channel tag [for global tags, use all for channel]'}
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
            padding = max(list(map(lambda x: len(x), list(ACCEPTABLE_COMMANDS.keys()))))+1
            for k, v in ACCEPTABLE_COMMANDS.items():
                msg += '{message: <{padding}}| Usage - {description}\n'.format(message=k, padding=padding, description=v['desc'])
            msg += '```'
            return msg

        def permission(message):
            def help_(message):
                msg = "**PERMISSION HELP**\n> Available commands:\n```"
                padding = max(list(map(lambda x: len(x), list(ACCEPTABLE_COMMANDS.keys()))))+1
                for k, v in ACCEPTABLE_COMMANDS.items():
                    msg += '{message: <{padding}}| Usage - {description}\n'.format(message=k, padding=padding, description=v['desc'])
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
                'help' : {'func': help_, 'desc': self.admin_cmd_tag+'permissions help'},
                'list' : {'func': list_permission, 'desc': self.admin_cmd_tag+'permissions list'},
                'add' : {'func': add_, 'desc': self.admin_cmd_tag+'permissions add role [CASE SENSITIVE]'},
                'remove' : {'func': remove_, 'desc': self.admin_cmd_tag+'permissions remove role [CASE SENSITIVE]'}
            }

            if len(message) == 0:
                return help_(message)

            cmd = message[0]
            if cmd in ACCEPTABLE_COMMANDS.keys():
                return ACCEPTABLE_COMMANDS[cmd]['func'](message[1:])
            else:
                return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

        ACCEPTABLE_COMMANDS = {
            'help' : {'func': help_, 'desc': self.admin_cmd_tag+'help'},
            'filterbot' : {'func': filterbot, 'desc': self.admin_cmd_tag+'filterbot'},
            'permissions' : {'func': permission, 'desc': self.admin_cmd_tag+'permissions'}
        }
        
        cmd = content.split(' ')[0]
        if cmd in ACCEPTABLE_COMMANDS.keys():
            return ACCEPTABLE_COMMANDS[cmd]['func'](content.split(' ')[1:])
        else:
            return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys())))

    def command_reader(self, content):
        def help_(message):
            msg = "**TOOLKIT HELP**\n> Available commands:\n```"
            for k, v in ACCEPTABLE_COMMANDS.items():
                msg += '{}: Usage - {}\n'.format(k, v['desc'])
            msg += '```'
            return msg, None
        
        def schedule(message):
            available_text = {
                "monday" : './data/schedule/monday.jpg',
                "mon" : './data/schedule/monday.jpg',
                "tuesday" : './data/schedule/tuesday.jpg',
                "tue" : './data/schedule/tuesday.jpg',
                "wednesday" : './data/schedule/wednesday.jpg',
                "wed" : './data/schedule/wednesday.jpg',
                "thursday" : './data/schedule/thursday.jpg',
                "thu" : './data/schedule/thursday.jpg',
                "friday" : './data/schedule/friday.jpg',
                "fri" : './data/schedule/friday.jpg',
                "saturday" : './data/schedule/saturday.jpg',
                "sat" : './data/schedule/saturday.jpg',
                "sunday" : './data/schedule/sunday.jpg',
                "sun" : './data/schedule/sunday.jpg'
            }
            if len(message) > 1 or message[0] not in available_text.keys():
                return 'incorrect format is given, please check {}help'.format(self.cmd_tag), None
            else:
                return None, discord.File(available_text[message[0]])


        ACCEPTABLE_COMMANDS = {
            'help' : {'func': help_, 'desc': self.cmd_tag+'help'},
            'schedule' : {'func': schedule, 'desc': self.cmd_tag+'schedule day [day format is 3 letter day (e.g. thu) or full name (e.g. thursday)]'}
        }
        
        cmd = content.split(' ')[0]
        if cmd in ACCEPTABLE_COMMANDS.keys():
            return ACCEPTABLE_COMMANDS[cmd]['func'](content.split(' ')[1:])
        else:
            return 'incorect command given, please choose command from list: {}'.format(", ".join(list(ACCEPTABLE_COMMANDS.keys()))), None

    # initialization
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        activity = discord.Game(name="llc-help | llca-help")
        await self.change_presence(activity=activity)

    async def on_message(self, message):
        ### implement checks
        # prevent recursive case
        if message.author == self.user:
            return

        # admin command central
        if message.content[:len(self.admin_cmd_tag)] == self.admin_cmd_tag:
            not_found = True
            for role in message.author.roles:
                if role.name in self.allowed_roles and not_found:
                    reply = self.admin_command_reader(message.content[len(self.admin_cmd_tag):])
                    await message.channel.send(reply)
                    not_found = False
            if not_found:
                await message.channel.send(f"Hi {message.author.mention}, you do not have the required permission to use this command!")
        
        # regular command central
        if message.content[:len(self.cmd_tag)] == self.cmd_tag:
            reply, file_reply = self.command_reader(message.content[len(self.cmd_tag):])
            if reply is not None and file_reply is None:
                await message.channel.send(reply)
            elif file_reply is not None and reply is None:
                await message.channel.send(file=file_reply)
            else:
                await message.channel.send(reply, file=file_reply)
            
        # filter nhentai tags
        urls = find_url(message.content)
        if len(urls) > 0:
            if self.verbose:
                print('found nhentai links', urls)
            # check to see if message contains bad content
            to_pass, problems = scan_links(urls, message.channel.name, self.forbidden_tags)

            # format problems
            if len(problems) == 1:
                msg = problems[0]
            elif len(problems) > 1:
                msg = ", ".join(problems[:-1]) + " and " + problems[-1]

            if to_pass:
                if self.verbose:
                    print('a problemmatic tag was found')
                await message.delete()
                # await message.channel.send(f"Hi {message.author.mention}, your nhentai link(s) contain(s) the {msg} tag(s), please do not send links with these tag(s)!")
                # await message.channel.send(f"H, hey {message.author.mention}... I, it's not like I want you to stop sending nhentai link(s) containing the {msg} tag(s)!")
                await message.channel.send(f"Hi {message.author.mention}, your nhentai link(s) contain(s) the {msg} tag(s), which is(are) against discord ToS/channel rules. Please refrain from posting such links in the future.")
        
            