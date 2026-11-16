---
description: Guided setup. Asks the lead five plain questions and writes team.config.yaml.
---

Run the guided setup for this agent team.

1. Read `team.config.example.yaml`. If `team.config.yaml` exists, read it too and treat its values as the current answers.
2. Fill `github_owner` and `template_repo` yourself from `git remote get-url origin`. Do not ask the lead for them.
3. Ask the lead these five questions in plain language, one message, numbered. Offer the current answer as the default where there is one.
   1. What name should appear as project lead?
   2. Should the decision register be copied to a Google Sheet? If yes, which email should the sheet be shared with?
   3. Should each decision memo also become a task in your task tracker? If yes, which tracker (a link)?
   4. Should urgent memos send an alert to your phone?
   5. Should the team continue the work on a schedule? If yes, what time each day, and in which time zone?
4. Write `team.config.yaml` from the answers, keeping the example's structure and comments. Set `track_changes_author` to the lead's name unless the lead names someone else. Leave `sheet_id` empty; the Drive add-on fills it when it first creates the sheet.
5. Show the lead the finished file in a short summary, not the raw YAML, and ask for a "go".
6. On "go", commit it: `git add team.config.yaml && git commit -m "Setup: team settings"` and push. New project repositories made from this template inherit these settings.

Do not switch on an add-on whose connector or tool is not available in this session. Say which one is missing and leave it off.

$ARGUMENTS
