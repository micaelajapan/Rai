import discord
from discord.ext import commands
import os
import json
from .utils import helper_functions as hf

dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__))).replace('\\', '/')


class Jpserv:
    """Modules unique for the Japanese server"""

    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        return ctx.guild.id == 189571157446492161 or ctx.guild.id == 275146036178059265
        # these commands are only useable on Japanese server or my testing server

    def is_admin():
        async def pred(ctx):
            return ctx.channel.permissions_for(ctx.author).administrator

        return commands.check(pred)

    @commands.command()
    @hf.is_admin()
    async def swap(self, ctx):
        if self.bot.jpJHO.permissions_for(ctx.author).administrator:
            if self.bot.jpJHO.position == 4:
                await self.bot.jpJHO.edit(position=5, name='just_hanging_out_2')
                await self.bot.jpJHO2.edit(position=4, name='just_hanging_out')
            else:
                await self.bot.jpJHO.edit(position=4, name='just_hanging_out')
                await self.bot.jpJHO2.edit(position=5, name='just_hanging_out_2')

    @commands.group(invoke_without_command=True, aliases=['uhc'])
    async def ultrahardcore(self, ctx, member: discord.Member = None):
        """Irreversible hardcore mode.  Must talk to an admin to have this undone."""
        role = ctx.guild.get_role(486851965121331200)
        ID = self.bot.db['mod_role'][str(ctx.guild.id)]['id']
        mod_role = ctx.guild.get_role(ID)
        if member:  # if you specified someone else's ID, then remove UHC from them
            if mod_role in ctx.author.roles or ctx.channel.permissions_for(ctx.author).administrator:
                if ctx.author.id != member.id:
                    self.bot.db['ultraHardcore'][str(self.bot.ID["jpServ"])].remove(member.id)
                    hf.dump_json()
                    try:
                        await member.remove_roles(role)
                    except discord.errors.Forbidden:
                        await ctx.send("I couldn't remove the ultra hardcore role")
                    await ctx.send(f'Undid ultra hardcore mode for {member.name}')
            else:
                await ctx.send(f"You can not remove UHC from other members.  Only mods/admins can.")
        else:
            await ctx.send(f"This is ultra hardcore mode.  It means you must speak in the language you are learning "
                           f"(for example, if you are learning Japanese, any messages in English will be deleted). "
                           f"This can not be undone except for asking a mod to remove it for you.  \n\n"
                           f"To enable ultra hardcore mode, type `;uhc on` or `;uhc enable`.  ")

    @ultrahardcore.command(aliases=['enable'])
    async def on(self, ctx):
        role = ctx.guild.get_role(486851965121331200)
        if ctx.author.id not in self.bot.db['ultraHardcore'][str(self.bot.ID["jpServ"])]:  # if not enabled
            self.bot.db['ultraHardcore'][str(self.bot.ID["jpServ"])].append(ctx.author.id)
            hf.dump_json()
            try:
                await ctx.author.add_roles(role)
            except discord.errors.Forbidden:
                await ctx.send("I couldn't add the ultra hardcore role")
            await ctx.send(f"{ctx.author.name} has chosen to enable ultra hardcore mode.  It works the same as "
                           "normal hardcore mode except that you can't undo it and asterisks don't change "
                           "anything.  Talk to a mod to undo this.")
        else:  # already enabled
            await ctx.send("You're already in ultra hardcore mode.")

    @ultrahardcore.command()
    async def list(self, ctx):
        """Lists the people currently in ultra hardcore mode"""
        string = 'The members in ultra hardcore mode right now are '
        guild = self.bot.get_guild(189571157446492161)
        members = []

        for member_id in self.bot.db['ultraHardcore'][str(guild.id)]:
            member = guild.get_member(int(member_id))
            if member is not None:  # in case a member leaves
                members.append(str(member))
            else:
                self.bot.db['ultraHardcore'][str(guild.id)].remove(member_id)
                await ctx.send(f'Removed <@{member_id}> from the list, as they seem to have left the server')

        await ctx.send(string + ', '.join(members))

    @ultrahardcore.command()
    async def explanation(self, ctx):
        """Explains ultra hardcore mode for those who are using it and can't explain it"""
        if ctx.author.id in self.bot.db['ultraHardcore'][str(ctx.guild.id)]:
            await ctx.send(f"{ctx.author.mention} is currently using ultra hardcore mode.  In this mode, they can't "
                           f"speak any English, and they also cannot undo this mode themselves.")
        else:
            await ctx.send(f"{ctx.author.mention} is currently NOT using hardcore mode, so I don't know why "
                           f"they're trying to use this command.  But, ultra hardcore mode means a user can't speak "
                           f"any English, and can't undo this mode themselves no matter what.")

    @ultrahardcore.command()
    @hf.is_admin()
    async def ignore(self, ctx):
        config = self.bot.db['ultraHardcore']
        try:
            if ctx.channel.id not in config['ignore']:
                config['ignore'].append(ctx.channel.id)
                await ctx.send(f"Added {ctx.channel.name} to list of ignored channels for UHC")
            else:
                config['ignore'].remove(ctx.channel.id)
                await ctx.send(f"Removed {ctx.channel.name} from list of ignored channels for UHC")
        except KeyError:
            config['ignore'] = [ctx.channel.id]
            await ctx.send(f"Added {ctx.channel.name} to list of ignored channels for UHC")
        hf.dump_json()

def setup(bot):
    bot.add_cog(Jpserv(bot))
