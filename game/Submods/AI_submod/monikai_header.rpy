init -990 python in mas_submod_utils:
    Submod(
        author="Rubiksman1006",
        name="AI_submod",
        description="AI based features for MAS.",
        settings_pane="monikai_chat_settings",
        version="1.3.5",
        version_updates = {}
    )

# Register the updater
init -989 python:
    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="AI_submod",
            user_name="Rubiksman78",
            repository_name="MonikA.I",
            update_dir="",
        )