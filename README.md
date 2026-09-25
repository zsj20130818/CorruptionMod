# CorruptionMod - Netease Minecraft Bedrock Edition

A psychological horror mod ported from Java Edition to Netease Bedrock Edition.

## Features
- Corruption system
- Verity companion summoning
- Dialogue system
- Jump scare events

## Known Issues

### 🔴 Critical
- **`ImportError: No module named verity_network`**
  - Location: `event/scare_director.py` line 16
  - Impact: Server-side init fails entirely, all server events dead
  - Status: Under investigation

### 🟠 Major
- **Tick crash loop on world exit**
  - `client/clientApp.py:761` → `'NoneType' has no attribute 'Tick'`
  - `client/appmgr/effectMgr.py:67` → `'NoneType' has no attribute 'time'`
  - Triggered after `ecs_framework clear all`, floods log every frame
- **UI null-pointer on screen push/pop**
  - `client/clientApp.py:1403` `OnHandlePushScreen`
  - `client/clientApp.py:1417` `OnPopScreenAfter`
  - `vipLogic/utils/foldMenuScreenMgr.py:61`

### 🟡 Minor
- **`minecraft:despawn` config invalid**
  - Affected entities: `verity:hallucination`, `verity:boss`, `verity:companion`
  - Error: `child 'never_despawn' not valid here`
- Custom spawn egg not showing in creative inventory
- Entity model failed to load

## How to Help
1. Fork this repository
2. Create your feature branch
3. Commit your changes
4. Open a Pull Request

## License
CC BY-NC-SA 4.0

## Contact
- GitHub Issues: Open an issue directly in this repository
- Email: zsj201308182026@163.com (Project related only)
