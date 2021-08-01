﻿using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using VexTrack.Core;
using VexTrack.MVVM.ViewModel.Popups;

namespace VexTrack.MVVM.ViewModel
{
	class SeasonViewModel : ObservableObject
	{
		public RelayCommand SeasonButtonClick { get; set; }

		//public SeasonPopupViewModel SeasonPopup { get; set; }
		//public EditableSeasonPopupViewModel EditableSeasonPopup { get; set; }
		private MainViewModel MainVM { get; set; }

		private ObservableCollection<SeasonEntryData> _entries = new();
		public ObservableCollection<SeasonEntryData> Entries
		{
			get => _entries;
			set
			{
				if (_entries != value)
				{
					_entries = value;
					OnPropertyChanged();
				}
			}
		}

		public SeasonViewModel()
		{
			MainVM = (MainViewModel)ViewModelManager.ViewModels["Main"];
			//SeasonPopup = (SeasonPopupViewModel)ViewModelManager.ViewModels["SeasonPopup"];
			//EditableSeasonPopup = (EditableSeasonPopupViewModel)ViewModelManager.ViewModels["EditableSeasonPopup"];

			SeasonButtonClick = new RelayCommand(OnSeasonButtonClick);
			Update(false);
		}

		public void Update(bool epilogue)
		{
			Entries.Clear();

			foreach (Season s in TrackingDataHelper.Data.Seasons)
			{
				Entries.Add(SeasonDataCalc.CalcSeason(s, epilogue));
			}
		}

		public void OnSeasonButtonClick(object parameter)
		{
			string uuid = (string)parameter;

			//SeasonPopup.SetFlags(true, true);
			//SeasonPopup.SetData(Entries.Where(e => e.UUID == uuid).First());
			//MainVM.QueuePopup(SeasonPopup);
		}
	}
}
