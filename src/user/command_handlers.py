# class VoteForUserCommandHandler(1`):
#
#     async def __call__(self, command: VoteForUserCommand) -> UserStatisticsModel:
#         """
#         1) Checks, if a vote is appropriate.
#         2) Likes or dislikes user, depends on from command data.
#         3) Creates event, signaling that user has voted.
#         """
#
#     async with self._uow as uow:
#         if command.voting_user_id == command.voted_for_user_id:
#             raise UserCanNotVoteForHimSelf
#
#         users_service: UsersService = UsersService(uow=uow)
#         if await users_service.check_if_user_already_voted(
#                 voting_user_id=command.voting_user_id,
#                 voted_for_user_id=command.voted_for_user_id
#         ):
#             raise UserAlreadyVotedError
#
#         user_statistics: UserStatisticsModel
#         if command.liked:
#             user_statistics = await users_service.like_user(
#                 voting_user_id=command.voting_user_id,
#                 voted_for_user_id=command.voted_for_user_id
#             )
#         else:
#             user_statistics = await users_service.dislike_user(
#                 voting_user_id=command.voting_user_id,
#                 voted_for_user_id=command.voted_for_user_id
#             )
#
#         voted_for_user: UserModel = await users_service.get_user_by_id(id=command.voted_for_user_id)
#         voting_user: UserModel = await users_service.get_user_by_id(id=command.voting_user_id)
#         await uow.add_event(
#             UserVotedEvent(
#                 liked=command.liked,
#                 disliked=command.disliked,
#                 voted_for_user_email=voted_for_user.email,
#                 voted_for_user_username=voted_for_user.username,
#                 voting_user_username=voting_user.username,
#                 voting_user_email=voting_user.email,
#             )
#         )
#
#         return user_statistics