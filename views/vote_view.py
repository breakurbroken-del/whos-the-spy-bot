import discord


class VoteView(discord.ui.View):

    def __init__(self, session):

        super().__init__(timeout=15)

        self.session = session

    async def vote_player(
        self,
        interaction,
        target_index
    ):

        voter_id = interaction.user.id

        if voter_id not in self.session.players:

            return await interaction.response.send_message(
                "You are not in this game.",
                ephemeral=True
            )

        if voter_id in self.session.voted_players:

            return await interaction.response.send_message(
                "You already voted.",
                ephemeral=True
            )

        if target_index >= len(
            self.session.speaking_queue
        ):

            return await interaction.response.send_message(
                "Invalid Vote.",
                ephemeral=True
            )

        target_id = (
            self.session.speaking_queue[
                target_index
            ]
        )

        if target_id in self.session.eliminated_players:

            return await interaction.response.send_message(
                "Player already eliminated.",
                ephemeral=True
            )

        self.session.voted_players.append(
            voter_id
        )

        self.session.votes[target_id] = (
            self.session.votes.get(
                target_id,
                0
            ) + 1
        )

        await interaction.response.send_message(
            "✅ Vote Submitted",
            ephemeral=True
        )

    @discord.ui.button(
        label="1️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_1(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            0
        )

    @discord.ui.button(
        label="2️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_2(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            1
        )

    @discord.ui.button(
        label="3️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_3(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            2
        )

    @discord.ui.button(
        label="4️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_4(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            3
        )

    @discord.ui.button(
        label="5️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_5(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            4
        )

    @discord.ui.button(
        label="6️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_6(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            5
        )

    @discord.ui.button(
        label="7️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_7(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            6
        )

    @discord.ui.button(
        label="8️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_8(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            7
        )

    @discord.ui.button(
        label="9️⃣",
        style=discord.ButtonStyle.primary
    )
    async def vote_9(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            8
        )

    @discord.ui.button(
        label="🔟",
        style=discord.ButtonStyle.primary
    )
    async def vote_10(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):
        await self.vote_player(
            interaction,
            9
        )
