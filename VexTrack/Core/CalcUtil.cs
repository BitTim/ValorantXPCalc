﻿using System;

namespace VexTrack.Core
{
	public static class CalcUtil
	{
		public static int CumulativeSum(int index, int offset, int amount)
		{
			var ret = 0;
			for (var i = 2; i <= index; i++)
			{
				ret += (amount * i) + offset;
			}

			return ret;
		}

		public static int CalcTotalCollected(int activeLevel, int cxp)
		{
			int collected;
			if (activeLevel - 1 <= Constants.BattlepassLevels) collected = CalcUtil.CumulativeSum(activeLevel - 1, Constants.Level2Offset, Constants.XpPerLevel) + cxp;
			else collected = CalcMaxForSeason(false) + cxp + (activeLevel - Constants.BattlepassLevels - 1) * Constants.XpPerEpilogueLevel;

			return collected;
		}

		public static double CalcProgress(double total, double collected)
		{
			if (total <= 0) return 100;

			var ret = Math.Floor(collected / total * 100);
			return ret;
		}

		public static int CalcMaxForLevel(int level)
		{
			return Constants.Level2Offset + (level * Constants.XpPerLevel);
		}

		public static int CalcMaxForTier(int tier)
		{
			return tier switch
			{
				1 => 20000,
				2 => 30000,
				3 => 40000,
				4 => 50000,
				5 => 60000,
				6 => 75000,
				7 => 100000,
				8 => 150000,
				9 => 200000,
				10 => 250000,
				_ => 0
			};
		}

		public static int CalcMaxForSeason(bool epilogue)
		{
			var sum = CumulativeSum(Constants.BattlepassLevels, Constants.Level2Offset, Constants.XpPerLevel);
			if (epilogue) sum += Constants.EpilogueLevels * Constants.XpPerEpilogueLevel;

			return sum;
		}
	}
}