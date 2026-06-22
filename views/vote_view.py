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
