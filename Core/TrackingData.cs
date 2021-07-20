﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using Newtonsoft.Json.Linq;

namespace VexTrack.Core
{
	class HistoryEntry
	{
		public long Time { get; set; }
		public string Description { get; set; }
		public int Amount { get; set; }

		public string Map { get; set; }

		public HistoryEntry(long time, string desc, int amount, string map)
		{
			(Time, Description, Amount, Map) = (time, desc, amount, map);
		}
	}

	class Goal
	{
		public string Name { get; set; }
		public int Remaining { get; set; }
		public int StartXP { get; set; }
		public string Color { get; set; }

		public Goal(string name, int remaining, int startXP, string color)
		{
			(Name, Remaining, StartXP, Color) = (name, remaining, startXP, color);
		}
	}

	class Season
	{
		public string Name { get; set; }
		public string EndDate { get; set; }
		public int ActiveBPLevel { get; set; }
		public int CXP { get; set; }
		public List<HistoryEntry> History { get; set; }

		public Season(string name, string endDate, int activeBPLevel, int cXP, List<HistoryEntry> history)
		{
			(Name, EndDate, ActiveBPLevel, CXP, History) = (name, endDate, activeBPLevel, cXP, history);
		}
	}

	class TrackingData
	{
		public List<Goal> Goals { get; set; }
		public List<Season> Seasons { get; set; }

		public TrackingData(List<Goal> goals, List<Season> seasons)
		{
			(Goals, Seasons) = (goals, seasons);
		}
	}

	class TrackingDataHelper
	{
		public TrackingData Tracking { get; set; }

		public void initData(string path, string seasonName, string seasonEndDate, int activeBPLevel, int cXP)
		{
			List<Goal> goals = new();
			List<Season> seasons = new();

			List<HistoryEntry> history = new();
			history.Add(new HistoryEntry(DateTimeOffset.Now.ToUnixTimeSeconds(), "Initialization", cXP, null));
			seasons.Add(new Season(seasonName, seasonEndDate, activeBPLevel, cXP, history));

			Tracking = new TrackingData(goals, seasons);
			saveData(path);
		}

		public void loadData(string path)
		{
			if (!File.Exists(path) || File.ReadAllText(path) == "")
			{
				//TODO: Convert Legacy config.json to data.json
				initData(path, "First Season", "01.01.1970", 2, 0);
			}

			string rawJSON = File.ReadAllText(path);
			JObject jo = JObject.Parse(rawJSON);

			List<Goal> goals = new();
			foreach(JObject goal in jo["goals"]) {
				string name = (string)goal["name"];
				int remaining = (int)goal["remaining"];
				int startXP = (int)goal["startXP"];
				string color = (string)goal["color"];

				goals.Add(new Goal(name, remaining, startXP, color));
			}

			List<Season> seasons = new();
			foreach (JObject season in jo["seasons"]) {
				string name = (string)season["name"];
				string endDate = (string)season["endDate"];
				int activeBPLevel = (int)season["activeBPLevel"];
				int cXP = (int)season["cXP"];

				string historyKey = "history";
				if (season["history"] == null)
				{
					historyKey = "xpHistory";
				}

				List<HistoryEntry> history = new();
				foreach(JObject historyEntry in season[historyKey])
				{
					long time = (long)historyEntry["time"];
					string description = (string)historyEntry["description"];
					int amount = (int)historyEntry["amount"];
					string map = (string)historyEntry["map"];

					history.Add(new HistoryEntry(time, description, amount, map));
				}

				seasons.Add(new Season(name, endDate, activeBPLevel, cXP, history));
			}

			Tracking = new TrackingData(goals, seasons);
		}

		public void saveData(string path)
		{
			JObject jo = new();

			JArray goals = new();
			foreach(Goal goal in Tracking.Goals)
			{
				JObject goalObj = new();
				goalObj.Add("name", goal.Name);
				goalObj.Add("remaining", goal.Remaining);
				goalObj.Add("startXP", goal.StartXP);
				goalObj.Add("color", goal.Color);

				goals.Add(goalObj);
			}

			jo.Add("goals", goals);

			JArray seasons = new();
			foreach (Season season in Tracking.Seasons)
			{
				JObject seasonObj = new();
				seasonObj.Add("name", season.Name);
				seasonObj.Add("endDate", season.EndDate);
				seasonObj.Add("activeBPLevel", season.ActiveBPLevel);
				seasonObj.Add("cXP", season.CXP);

				JArray history = new();
				foreach (HistoryEntry historyEntry in season.History)
				{
					JObject historyEntryObj = new();
					historyEntryObj.Add("time", historyEntry.Time);
					historyEntryObj.Add("description", historyEntry.Description);
					historyEntryObj.Add("amount", historyEntry.Amount);
					historyEntryObj.Add("map", historyEntry.Map);

					history.Add(historyEntryObj);
				}

				seasonObj.Add("history", history);
				seasons.Add(seasonObj);
			}

			jo.Add("seasons", seasons);

			if (!File.Exists(path))
			{
				int sep = path.LastIndexOf("/");

				Directory.CreateDirectory(path.Substring(0, sep));
				File.CreateText(path).Close();
			}

			File.WriteAllText(path, jo.ToString());
		}
	}
}
