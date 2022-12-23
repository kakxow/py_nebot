from .db import Session
from .nechat_db_types import Tag, User, MentionTag, user_from_dict


def list_tags() -> dict[str, list[MentionTag]]:
    with Session() as session:
        tags = session.query(Tag).all()
        return {
            (tag.name + (f" ({tag.group})" if tag.group else "")): tag.mentions
            for tag in tags
        }


def assign_tags(telegram_user: dict, chat_id: int, tags_to_assign: list[str]) -> str:
    with Session() as session:
        tags: list[Tag] = session.query(Tag).filter(Tag.name.in_(tags_to_assign)).all()
        if not tags:
            return "No existing tags in the command. Consider creating them with /create_tag or check existing tags with /list_tags."
        missing_tags_message = ""
        missing_tags = [t for t in tags_to_assign if t not in [t_.name for t_ in tags]]
        if missing_tags:
            missing_tags_message = "\nAlso, these tags do not exist - " + ", ".join(
                missing_tags
            )
        user = session.query(User).get(
            (telegram_user["id"], chat_id)
        ) or user_from_dict(telegram_user, chat_id)
        new_tags = set(tags) - set(user.tags)
        if not new_tags:
            return (
                "You already have these tags - "
                + ", ".join([tag.name for tag in tags])
                + missing_tags_message
            )
        already_have_tags = set(user.tags).intersection(tags)
        already_have_message = ""
        if already_have_tags:
            already_have_message = "\nYou already have these tags - " + ", ".join(
                [tag.name for tag in already_have_tags]
            )
        new_groups = [t.group for t in new_tags if t.group]
        tags_to_delete = [t.name for t in user.tags if t.group in new_groups]
        user.tags = [t for t in user.tags if t.group not in new_groups]
        user.tags.extend(new_tags)
        session.commit()
        return (
            "New tags added for user - "
            + ", ".join([tag.name for tag in new_tags])
            + "\nOld tags deleted from user - "
            + ", ".join(tags_to_delete)
            + already_have_message
            + missing_tags_message
        )


def create_tag(
    tag_name: str, mentions_for_new_tag: list[str], group: str | None = None
) -> str:
    with Session() as session:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        if tag:
            mentions_of_existing_tag = ", ".join([m.name for m in tag.mentions])
            return f"Tag with this name already exists. You can mention it with {mentions_of_existing_tag}"
        clean_mentions = [m.replace("@", "") for m in mentions_for_new_tag]
        existing_mentions = (
            session.query(MentionTag).filter(MentionTag.name in clean_mentions).all()
        )
        if existing_mentions:
            mention_for_tag = "\n".join(
                [f"{m.name} for {m.tag.name}" for m in existing_mentions]
            )
            return f"These mentions are already in use:\n{mention_for_tag}"
        new_tag = Tag(
            name=tag_name,
            mentions=[MentionTag(name=m) for m in clean_mentions],
            group=group,
        )
        session.add(new_tag)
        session.commit()
        return f"New tag {tag_name} created. You can assign it for yourself with /assign_tag [tag_name] command."


def free_tags(telegram_user: dict, chat_id: int, tags: list[str]) -> str:
    with Session() as session:
        user = session.query(User).get(
            (telegram_user["id"], chat_id)
        ) or user_from_dict(telegram_user, chat_id)
        tags_to_remove = {t.name for t in user.tags}.intersection(tags)
        if not tags_to_remove:
            return "You don't have any of these tags - " + ", ".join(tags)
        user.tags = [t for t in user.tags if t.name not in tags]
        session.commit()
        return "Tags removed: " + ", ".join(tags_to_remove)


def free_all_tags(telegram_user: dict, chat_id: int) -> str:
    with Session() as session:
        user = session.query(User).get(
            (telegram_user["id"], chat_id)
        ) or user_from_dict(telegram_user, chat_id)
        if not user.tags:
            return "You did not have any tags."
        tags_to_remove = ", ".join([t.name for t in user.tags])
        user.tags = []
        session.commit()
        return "All tags removed from you - " + tags_to_remove


def update_tag(tag_name: str, new_mentions: list[str]) -> str:
    with Session() as session:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return f"Tag with name {tag_name} does not exist."
        clean_mentions = [m.replace("@", "") for m in new_mentions]
        occupied_mentions = (
            session.query(MentionTag)
            .filter(MentionTag.name.in_(clean_mentions), MentionTag.tag_id != tag.id)
            .all()
        )
        if occupied_mentions:
            return "These mentions are occupied by other tags:\n" + "\n".join(
                [f"{m.name} for {m.tag.name}" for m in occupied_mentions]
            )
        existing_mentions = [m for m in tag.mentions if m.name in (new_mentions)]
        existing_mentions_names = [m.name for m in existing_mentions]
        mentions_to_add = [m for m in new_mentions if m not in existing_mentions_names]
        tag.mentions = [MentionTag(name=name) for name in mentions_to_add]
        tag.mentions.extend(existing_mentions)
        session.commit()
        return f'"{tag_name}" tag updated with new list of mentions - ' + ", ".join(
            new_mentions
        )


def your_tags(telegram_user: dict, chat_id: int) -> str:
    with Session() as session:
        user = session.query(User).get(
            (telegram_user["id"], chat_id)
        ) or user_from_dict(telegram_user, chat_id)
        if not user.tags:
            return "You do not have any tags."
        reply = ""
        for tag in user.tags:
            list_of_mentions = ", ".join(
                [mention.name for mention in tag.mentions]
            ).replace("@", "")
            reply = reply + f"<b>{tag.name}</b>\t{list_of_mentions}\n\n"
        return "Your tags are:\n" + reply


def tagger(chat_id: int, mentions: list[str]) -> list[User]:
    clean_mentions = [m.replace("@", "") for m in mentions]
    with Session() as session:
        return (
            session.query(User)
            .filter(User.chat == chat_id)
            .join(User.tags)
            .join(Tag.mentions)
            .filter(User.chat == chat_id, MentionTag.name.in_(clean_mentions))
            .all()
        )


def delete_tag(tag_name: str) -> str:
    with Session() as session:
        tag = session.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            return "No tag named " + tag_name
        session.delete(tag)
        session.commit()
        return "Tag deleted - " + tag_name
