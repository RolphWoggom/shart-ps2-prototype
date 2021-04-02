// :: replace with __

struct radDate {
   short year;
   byte month;
   byte day;
   byte hour;
   byte minute;
   byte second;
};

enum CmdLineOptionEnum {
    NOMUSIC,
    NOEFFECTS,
    NODIALOG,
    MUTE,
    SKIPMOVIE,
    MEMMONITOR,
    HEAPSTATS,
    CDFILES,
    FIREWIRE,
    SNPROFILER,
    ARTSTATS,
    PROPSTATS,
    RANDOMBUTTONS,
    DEMOTEST,
    SEQUENTIALDEMO,
    SHORTDEMO,
    FEUNJOINED,
    FEGAGS,
    NOSPLASH,
    SKIPFE,
    SKIPLANGCHECK,
    SKIPMEMCHECK,
    SPEEDOMETER,
    NOHUD,
    NOTUTORIAL,
    COINS,
    DEBUGBV,
    SKIPSUNDAY,
    NOTRAFFIC,
    FPS,
    DESIGNER,
    DETECTLEAKS,
    NOHEAPS,
    PRINTMEMORY,
    NOHAPTIC,
    PCTEST,
    NOAVRIL,
    PRINTLOADTIME,
    PRINTFRAMERATE,
    SHOWDYNALOAD,
    MANUALRESETDAMAGE,
    NOPEDS,
    WINDOW,
    PROGSCAN,
    LARGEHEAPS,
    MEMCARDCHEAT,
    TOOL,
    FILENOTFOUND,
    LOADINGSPEW
};

enum VehicleAI__VehicleAITypeEnum {
    WAYPOINT,
    CHASE
};

enum Reward__eQuestType {
    DEFAULTCAR = 1,
    DEFAULTSKIN,
    CARDS,
    STREETRACE,
    BONUSMISSION,
    GOLDCARDS
};

enum Reward__eRewardType {
    SKIN = 1,
    CAR = 3,
    FE_TOY = 4
};

enum Merchandise__eSellerType {
    INTERIOR,
    SIMPSON,
    GIL
};

enum RespawnEntity__eRespawnEntity {
    UNKNWON1, // respawn time: 0xfffffffffffffd66
    WRENCH,
    WASP,
    UNKNWON2, // respawn time: 0xfffffffffffffd66
};

enum CharacterManager__CharacterType {
    PLAYER,
    NPC
};

enum CharacterSheetManager__eCollectableType {
    CARD //probably, only one found so far, there should be COIN, too
};

enum FileHandlerEnum {
    P3D_DEFAULT,
    P3D_LEVEL,
    P3D_MISSION,
    P3D,
    CHOREO,
    CONSOLE,
    SCROOBY,
    SOUND,
    P3D_TEMP,
    ICON
};
