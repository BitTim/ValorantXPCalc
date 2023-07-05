﻿using System.Collections.Generic;

namespace VexTrack.Core.Model.Game.Cosmetic.Weapon;

public class WeaponSkin : Cosmetic
{
    public string IconPath { get; set; }
    public string WallpaperPath { get; set; }
    
    public List<WeaponSkinChroma> Chromas { get; set; }
    public List<WeaponSkinLevel> Levels { get; set; }

    public WeaponSkin(string uuid, string name, string iconPath, string wallpaperPath, List<WeaponSkinChroma> chromas, List<WeaponSkinLevel> levels) : base(uuid, name, "WeaponSkin")
    {
        IconPath = iconPath;
        WallpaperPath = wallpaperPath;
        Chromas = chromas;
        Levels = levels;
    }
}