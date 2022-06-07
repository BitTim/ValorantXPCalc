package com.bittim.vextrack.fragments.settings

import android.os.Bundle
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.bittim.vextrack.R
import com.bittim.vextrack.databinding.FragmentSettingsGeneralBinding

class GeneralFragment : Fragment()
{
	override fun onCreate(savedInstanceState: Bundle?)
	{
		super.onCreate(savedInstanceState)
	}

	private var _binding: FragmentSettingsGeneralBinding? = null
	private val binding get() = _binding!!

	override fun onCreateView(
		inflater: LayoutInflater, container: ViewGroup?,
		savedInstanceState: Bundle?
	): View
	{
		_binding = FragmentSettingsGeneralBinding.inflate(inflater, container, false)

		return binding.root
	}

	override fun onDestroyView()
	{
		super.onDestroyView()
		_binding = null
	}
}