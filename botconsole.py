import asyncio
import discord
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
from rich.theme import Theme
from rich import box
import sys
import os
import random
import json
from datetime import datetime

# Pro Console Theme
pro_theme = Theme({
    "primary": "#ffffff bold", 
    "secondary": "#00d7ff", 
    "accent": "#5fafff", 
    "muted": "#8a8a8a",
    "success": "bold #00ff87",
    "danger": "bold #ff5f5f",
    "warning": "bold #ffaf00"
})

console = Console(theme=pro_theme)

# Clean, professional header
HEADER_TITLE = """
[secondary]
██████╗  ██████╗ ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗ ██████╗ ██╗     ███████╗
██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██╔═══██╗████╗  ██║██╔════╝██╔═══██╗██║     ██╔════╝
██████╔╝██║   ██║   ██║   ██║     ██║   ██║██╔██╗ ██║███████╗██║   ██║██║     █████╗  
██╔══██╗██║   ██║   ██║   ██║     ██║   ██║██║╚██╗██║╚════██║██║   ██║██║     ██╔══╝  
██████╔╝╚██████╔╝   ██║   ╚██████╗╚██████╔╝██║ ╚████║███████║╚██████╔╝███████╗███████╗
╚═════╝  ╚═════╝    ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝
[/secondary]
"""

class BotConsole:
    def __init__(self):
        self.client = discord.Client(intents=discord.Intents.all())
        self.token = None
        self.active_channel = None
        self.is_running = True
        self.start_time = datetime.now()

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def draw_header(self, subtitle="READY"):
        self.clear_screen()
        console.print(Align.center(HEADER_TITLE))
        console.print(Align.center(Text(f" {subtitle} ", style="on #3a3a3a white bold")))
        console.print("\n")

    async def start(self):
        self.draw_header("AUTHENTICATION")
        
        self.token = await questionary.password(
            "Enter Bot Token:",
            style=questionary.Style([('password', 'fg:#00d7ff')])
        ).ask_async()
        
        if not self.token:
            console.print("[danger]Error: No token provided.[/danger]")
            return

        @self.client.event
        async def on_message(message):
            if self.active_channel and message.channel.id == self.active_channel.id:
                if message.author != self.client.user:
                    timestamp = datetime.now().strftime("%H:%M")
                    console.print(f"[muted]{timestamp}[/muted] [secondary]{message.author.name}[/secondary] [white]»[/white] {message.content}")

        with Progress(
            SpinnerColumn(spinner_name="simpleDotsScrolling", style="secondary"),
            TextColumn("[muted]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description="Connecting to Discord Gateway...", total=None)
            
            try:
                await self.client.login(self.token)
                loop = asyncio.get_event_loop()
                loop.create_task(self.client.connect())
                await asyncio.wait_for(self.client.wait_until_ready(), timeout=15.0)
                
                console.print(f"[success]Authenticated as:[/success] [white]{self.client.user}[/white]")
                await asyncio.sleep(0.5)
                await self.main_menu()
            except asyncio.TimeoutError:
                console.print("[danger]Connection Timeout: Check token and network.[/danger]")
            except Exception as e:
                console.print(f"[danger]Connection Failed: {e}[/danger]")
            finally:
                self.is_running = False
                await self.client.close()

    async def main_menu(self):
        while self.is_running:
            self.draw_header(f"Bot Session: {self.client.user}")
            
            choice = await questionary.select(
                "Select Command:",
                choices=[
                    questionary.Choice("💬  Live Chat", value="chat"),
                    questionary.Choice("👤  Profile Manager", value="profile"),
                    questionary.Choice("⚙️   Server Settings", value="modify"),
                    questionary.Choice("👥  Member List", value="intel"),
                    questionary.Choice("📜  Audit Logs", value="recon"),
                    questionary.Choice("⚠️   Advanced Tools", value="danger"),
                    questionary.Choice("🚪  Exit Console", value="exit"),
                ],
                style=questionary.Style([
                    ('pointer', 'fg:#00d7ff bold'),
                    ('highlighted', 'fg:#00d7ff bold'),
                    ('selected', 'fg:#ffffff bg:#00d7ff')
                ])
            ).ask_async()

            if choice == "chat": await self.chat_workflow()
            elif choice == "profile": await self.profile_workflow()
            elif choice == "modify": await self.modify_server_workflow()
            elif choice == "intel": await self.member_management_workflow()
            elif choice == "recon": await self.recon_workflow()
            elif choice == "danger": await self.danger_zone_workflow()
            elif choice == "exit":
                self.is_running = False
                console.print("[muted]Exiting console...[/muted]")

    async def profile_workflow(self):
        self.draw_header("PROFILE MANAGER")
        action = await questionary.select(
            "Settings:",
            choices=["Change Username", "Change Avatar", "Update Status", "Back"]
        ).ask_async()

        if action == "Change Username":
            name = await questionary.text("New Username:").ask_async()
            if name:
                await self.client.user.edit(username=name)
                console.print(f"[success]Username updated.[/success]")
        elif action == "Change Avatar":
            import aiohttp
            url = await questionary.text("Avatar Image URL:").ask_async()
            if url:
                async with aiohttp.ClientSession() as s:
                    async with s.get(url) as r:
                        if r.status == 200:
                            await self.client.user.edit(avatar=await r.read())
                            console.print("[success]Avatar updated.[/success]")
        elif action == "Update Status":
            name = await questionary.text("Status Message:").ask_async()
            if name:
                await self.client.change_presence(activity=discord.Game(name=name))
                console.print(f"[success]Status set to: {name}[/success]")
        await asyncio.sleep(1)

    async def select_guild(self):
        guilds = self.client.guilds
        if not guilds: return None
        choices = [questionary.Choice(g.name, value=g) for g in guilds]
        return await questionary.select("Select Server:", choices=choices).ask_async()

    async def select_channel(self, guild):
        channels = [c for c in guild.text_channels]
        if not channels: return None
        choices = [questionary.Choice(f"#{c.name}", value=c) for c in channels]
        return await questionary.select("Select Channel:", choices=choices).ask_async()

    async def chat_workflow(self):
        guild = await self.select_guild()
        if not guild: return
        channel = await self.select_channel(guild)
        if not channel: return
        
        self.active_channel = channel
        self.draw_header(f"Chat: #{channel.name}")
        
        console.print(Panel(
            f"[muted]Connection active. New messages will appear below.[/muted]\n[white]Use [/white][secondary]/exit[/secondary][white] to return to menu.[/white]",
            border_style="secondary", box=box.ROUNDED
        ))

        async for m in channel.history(limit=10):
            console.print(f"[muted]{m.created_at.strftime('%H:%M')}[/muted] [secondary]{m.author.name}[/secondary] » {m.content}")

        while True:
            t = await questionary.text("Input:", qmark="").ask_async()
            if not t or t.lower() == '/exit':
                self.active_channel = None
                break
            await channel.send(t)

    async def recon_workflow(self):
        guild = await self.select_guild()
        if not guild: return
        self.draw_header("AUDIT LOGS")
        
        table = Table(box=box.SIMPLE, header_style="secondary")
        table.add_column("TIME")
        table.add_column("USER")
        table.add_column("ACTION")
        
        async for entry in guild.audit_logs(limit=15):
            table.add_row(entry.created_at.strftime('%H:%M'), str(entry.user), str(entry.action).replace('AuditLogAction.', ''))
        
        console.print(table)
        await questionary.press_any_key_to_continue().ask_async()

    async def modify_server_workflow(self):
        guild = await self.select_guild()
        if not guild: return
        action = await questionary.select("Server Config:", choices=["Rename Server", "Create Channel", "Create Role", "Back"]).ask_async()
        
        if action == "Rename Server":
            n = await questionary.text("New Name:").ask_async()
            if n: await guild.edit(name=n)
        elif action == "Create Channel":
            n = await questionary.text("Channel Name:").ask_async()
            if n: await guild.create_text_channel(n)
        elif action == "Create Role":
            n = await questionary.text("Role Name:").ask_async()
            if n: await guild.create_role(name=n)
        console.print("[success]Operation successful.[/success]")
        await asyncio.sleep(1)

    async def danger_zone_workflow(self):
        guild = await self.select_guild()
        if not guild: return
        self.draw_header("ADVANCED TOOLS")
        
        console.print(Panel("[danger]Warning: The following tools perform destructive actions on the server.[/danger]", border_style="danger"))
        
        action = await questionary.select("Select Tool:", choices=["Clear Channel", "Nuke Server", "FULL DESTROY", "Back"]).ask_async()
        
        if action == "Clear Channel":
            c = await self.select_channel(guild)
            if c and await questionary.confirm("Purge messages?").ask_async():
                await c.purge()

        elif action == "Nuke Server":
            # ... (kept existing nuke logic for variety)
            code = "".join(random.choices("0123456789", k=4))
            console.print(f"[danger]CRITICAL OVERRIDE: Type this code to confirm WIPE:[/danger] [white on danger]{code}[/white on danger]")
            if await questionary.text("Code:").ask_async() == code:
                await self._execute_nuke(guild)

        elif action == "FULL DESTROY":
            code = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6))
            console.print(Panel(f"[bold red]!! ULTIMATUM !![/bold red]\nTHIS WILL BAN ALL MEMBERS, LOCKDOWN PERMISSIONS, AND WIPE THE SERVER.\n\nTYPE THIS CODE TO CONFIRM TOTAL DESTRUCTION: [bold yellow]{code}[/bold yellow]", border_style="danger"))
            if await questionary.text("Code:").ask_async() == code:
                console.print("[danger]INITIATING FULL DESTROY PROTOCOL...[/danger]")
                
                # 1. Ban all members (except bot)
                console.print("[danger]Executing Mass Ban Wave...[/danger]")
                for member in guild.members:
                    if member != guild.me:
                        try: await member.ban(reason="NUKED!")
                        except: pass

                # 2. Lockdown @everyone permissions
                try:
                    await guild.default_role.edit(permissions=discord.Permissions.none())
                    console.print("[success]Permissions locked down.[/success]")
                except: pass

                # 3. Identity & Wipe
                await self._execute_nuke(guild, full_destroy=True)

    async def _execute_nuke(self, guild, full_destroy=False):
        # Identity Wipe
        try: await guild.edit(name="NUKED", icon=None, banner=None, splash=None)
        except: pass

        # Delete Channels
        for c in guild.channels:
            try: await c.delete()
            except: pass
        
        # Wrapped in code block to prevent Discord markdown glitches
        nuke_art = """```
      _.-^^---....,,--
  _--                  --_
 <                        >)
 |                         |
  \._                   _./
     ```--. . , ; .--'''
           | |   |
        .-=|| | ||=-.
        `-=#$%&%$#=-'
           | ;  :|
  _____.,-#%&$@%#&#~,._____
```
"""
        spam_payload = f"@everyone\n{nuke_art}\n**THIS DOMAIN HAS COLLAPSED INTO THE VOID.**\n*Your permissions are revoked. Your community is dispersed.*\n**WELCOME TO THE SILENCE.**"

        # Create Channels and send message
        console.print(f"[danger]Reconstructing server architecture...[/danger]")
        for i in range(50 if full_destroy else 99): 
            try:
                new_c = await guild.create_text_channel("SENT-TO-RUIN")
                if full_destroy:
                    await new_c.send(spam_payload)
            except:
                break
        console.print("[success]Server neutralized.[/success]")
        await asyncio.sleep(1)

    async def member_management_workflow(self):
        guild = await self.select_guild()
        if not guild: return
        choices = [questionary.Choice(m.name, value=m) for m in guild.members[:50]]
        m = await questionary.select("Select Member:", choices=choices).ask_async()
        if m:
            act = await questionary.select(f"Action for {m.name}:", choices=["Kick", "Ban", "Back"]).ask_async()
            if act == "Kick": await m.kick()
            elif act == "Ban": await m.ban()
        await asyncio.sleep(1)

if __name__ == "__main__":
    app = BotConsole()
    try:
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(app.start())
        except RuntimeError:
            asyncio.run(app.start())
    except KeyboardInterrupt:
        pass
