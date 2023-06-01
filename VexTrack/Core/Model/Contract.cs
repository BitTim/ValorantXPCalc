﻿using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using VexTrack.Core.Helper;

namespace VexTrack.Core.Model;

public class Contract
{
    public string Uuid { get; set; }
    public string Type { get; set; }
    public string Name { get; set; }
    public long StartTimestamp { get; set; }
    public long EndTimestamp { get; set; }
    public string Color { get; set; }
    public bool Paused { get; set; }
    public List<Goal> Goals { get; set; }
    
    public int Total => GetTotal();
    public int Collected => GetCollected();
    public int Remaining => GetRemaining();
    public int Progress => CalcHelper.CalcProgress(Total, Collected);
    
    public string NextUnlockName => GetNextUnlock()?.Name ?? "None";
    public double NextUnlockProgress => GetNextUnlock()?.Progress ?? 100;
    public int NextUnlockRemaining => GetNextUnlock()?.Remaining ?? 0;
    
    public int Duration => GetDuration();
    public int RemainingDays => GetRemainingDays();
    public int CompletionForecastDays => GetCompletionForecastDays();
    public long CompletionTimestamp => GetCompletionTimestamp();
    public int BufferDays => (int)Math.Ceiling(Duration * (SettingsHelper.Data.BufferPercentage / 100));

    private bool IsActive => TimeHelper.NowTimestamp < EndTimestamp;
    public string Status => GetStatus();
    public ObservableCollection<Goal> ObservableGoals => new(Goals);
    


    public Contract(string uuid, string name, string color, bool paused, List<Goal> goals)
    {
        Uuid = uuid;
        Name = name;
        Color = color;
        Paused = paused;
        Goals = goals;
    }

    private int GetTotal() { return Goals.Sum(goal => goal.Total); }
    private int GetCollected() { return Goals.Sum(goal => goal.Collected); }
    private int GetRemaining() { return GetTotal() - GetCollected(); }

    
    private int GetCompletionForecastDays()
    {
        if (GetRemaining() <= 0) return -1;

        var average = UserData.CurrentSeasonData.Average;
        if (average <= 0) return -2;
        
        return (int)MathF.Ceiling((float)GetRemaining() / average);
    }

    private long GetCompletionTimestamp()
    {
        var nDays = CompletionForecastDays;
        return nDays < 0 ? nDays : TimeHelper.TodayDate.AddDays(nDays).ToUnixTimeSeconds();
    }

    private Goal GetNextUnlock()
    {
        return Goals.FirstOrDefault(goal => !goal.IsCompleted());
    }
    
    
    
    private int GetRemainingDays()
    {
        var endDate = TimeHelper.TimestampToDate(EndTimestamp);
        var today = TimeHelper.TodayDate;

        var remainingDays = (endDate - today).Days;
        if ((endDate - today).Hours > 12) { remainingDays += 1; }
        if (remainingDays < 0) remainingDays = 0;

        return remainingDays;
    }

    private int GetDuration()
    {
        var endDate = TimeHelper.TimestampToDate(EndTimestamp);
        var startDate = TimeHelper.TimestampToDate(StartTimestamp);

        var duration = (endDate - startDate).Days;
        if ((endDate - startDate).Hours > 12) { duration += 1; }
        if (duration < 0) duration = 0;

        return duration;
    }
    
    private string GetStatus()
    {
        if (Collected < /*TotalMin*/ 0) return IsActive ? "Warning" : "Failed"; //TODO: Rework
        if (Collected < Total) return "Done";
        return Collected >= Total ? "DoneAll" : "";
    }
}