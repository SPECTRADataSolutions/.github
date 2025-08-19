# contributing

## workflow
- all work starts as an **initiative**  
- initiatives may generate **epics** automatically  
- break epics down into **stories** and **tasks**  
- use only the provided issue templates for each work item type

## naming
- follow **camelCase** for all IDs, fields, and custom names
- issue titles: keep short, clear, and start with the correct emoji/type prefix
- no acronyms unless required by external standards
- do not abbreviate words like "organisation" to "org"; always spell them in full

## linking
- link stories and tasks back to their parent epic or initiative
- link epics back to their parent initiative
- dependencies between items must use the **🔗 Dependency** template

## labels
- use only labels from `.github/labels.json`
- do not create ad-hoc labels

## reviews
- small changes: 1 review from another contributor
- major changes: approval from the repo maintainer

## automation
- do not edit files in `outputs/` manually unless you are updating generated content intentionally
- workflows will reject incomplete or non-compliant issues

## conduct
- follow the [code of conduct](CODE_OF_CONDUCT.md)
