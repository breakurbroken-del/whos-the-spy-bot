import discord


class ReadyView(discord.ui.View):

    def __init__(self, session):

        super().__init__(timeout=30)

        self.session = session

    @discord.ui.button(
        label="Ready",
        emoji="🟢",
        style=discord.ButtonStyle.success
    )
    async def ready_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id not in self.session.players:

            return await interaction.response.send_message(
                "You are not part of this game.",
                ephemeral=True
            )

        if interaction.user.id in self.session.ready_players:

            return await interaction.response.send_message(
                "You are already ready.",
                ephemeral=True
            )

        self.session.ready_players.append(
            interaction.user.id
        )

        await interaction.response.send_message(
            "You are now ready.",
            ephemeral=True
        )

        # Everyone Ready

        if len(self.session.ready_players) == len(self.session.players):

            self.stop()

    @discord.ui.button(
        label="Leave",
        emoji="🔴",
        style=discord.ButtonStyle.danger
    )
    async def leave_button(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if interaction.user.id not in self.session.players:

            return await interaction.response.send_message(
                "You are not part of this game.",
                ephemeral=True
            )

        self.session.players.remove(
            interaction.user.id
        )

        await interaction.response.send_message(
            "You left the lobby.",
            ephemeral=True
        )

        self.stop()
