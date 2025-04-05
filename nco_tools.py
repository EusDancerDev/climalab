#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#-----------------------#
# Import custom modules #
#-----------------------#

from filewise.file_operations.ops_handler import add_to_path, rename_objects
from paramlib.global_parameters import basic_four_rules
from pygenutils.operative_systems.os_operations import run_system_command, exit_info
from pygenutils.strings.text_formatters import format_string, print_format_string

#-------------------------#
# Define custom functions #
#-------------------------#

def modify_variable_units_and_values(file_list,
                                     variable_name,
                                     operator,
                                     value,
                                     new_unit):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list)    
        
    for file_num, file_name in enumerate(file_list, start=1): 
        temp_file = add_to_path(file_name, str2add=file_name)
        
        is_whole_number = (abs(value-int(value)) == 0)
        use_integer_format = int(is_whole_number)
        
        var_chunit_formatted\
        = f"ncatted -a units,{variable_name},o,c,'{new_unit}' '{file_name}'"        
        process_exit_info = run_system_command(var_chunit_formatted,
                                               capture_output=True,
                                               encoding="utf-8")
        exit_info(process_exit_info)

        
        if operator not in basic_four_rules:
            raise ValueError(invalid_operator_err_template)
        else:            
            # Print progress information #
            operator_gerund = operator_gerund_dict.get(operator)
            format_args_print = (ncap2_base_args, 
                                 operator_gerund, value, variable_name, 
                                 file_num, lfl)
            print_format_string(prefmt_str_progress_UV, format_args_print)
            
            # Get the command from the corresponding switch case dictionary #
            format_args = (ncap2_base_args,
                           variable_name, variable_name, value,
                           file_name, temp_file)
            
            varval_mod_formatted = \
            format_string(varval_mod_command_templates_UV
                          .get(operator)
                          .get(use_integer_format),
                          format_args)
        
            # Execute the command through the shell #
            process_exit_info = run_system_command(varval_mod_formatted,
                                                   capture_output=True,
                                                   encoding="utf-8")
            exit_info(process_exit_info)            
            rename_objects(temp_file, file_name)
            

def modify_coordinate_values_by_threshold(file_list,
                                          dimension_name,
                                          threshold,
                                          operator,
                                          value,
                                          threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file_num, file_name in enumerate(file_list, start=1):
        temp_file = add_to_path(file_name, str2add=file_name)
        
        is_whole_number = (abs(value-int(value)) == 0)
        use_integer_format = int(is_whole_number)
        
        if operator not in basic_four_rules:
            raise ValueError(invalid_operator_err_template)
        else:
            if threshold_mode not in threshold_mode_opts:
                raise ValueError(format_string(invalid_threshold_mode_err_template,
                                               threshold_mode_opts))
            
            else:
                # Print progress information #
                operator_gerund = operator_gerund_dict.get(operator)
                    
                format_args_print = (ncap2_base_args, 
                                     operator_gerund, value, dimension_name, 
                                     file_num, lfl)
                
                print_format_string(prefmt_str_progress_BTH, format_args_print)
                
                # Get the command from the corresponding switch case dictionary #
                format_args = (ncap2_base_args,
                               dimension_name, threshold,
                               dimension_name, dimension_name, value,
                               file_name, temp_file)
        
                dimval_mod_formatted = \
                format_string(varval_mod_command_templates_BTH
                              .get(operator)
                              .get(threshold_mode)
                              .get(use_integer_format),
                              format_args)
            
                # Execute the command through the shell #
                process_exit_info = run_system_command(dimval_mod_formatted,
                                                       capture_output=True,
                                                       encoding="utf-8")
                exit_info(process_exit_info)                 
                rename_objects(temp_file, file_name)
            

def modify_coordinate_all_values(file_list,
                                 dimension_name,
                                 threshold,
                                 operator,
                                 value,
                                 threshold_mode="max"):
    
    if not isinstance(file_list, list):
        file_list = [file_list]
    lfl = len(file_list) 
    
    for file_num, file_name in enumerate(file_list, start=1): 
        temp_file = add_to_path(file_name, str2add=file_name)
        
        is_whole_number = (abs(value-int(value)) == 0)
        use_integer_format = int(is_whole_number)
        
        if operator not in basic_four_rules:
            raise ValueError(invalid_operator_err_template)
        else:
            if threshold_mode not in threshold_mode_opts:
                raise ValueError(format_string(invalid_threshold_mode_err_template,
                                               threshold_mode_opts))
            
            else:
                # Print progress information #
                operator_gerund = operator_gerund_dict.get(operator)
                    
                format_args_print = (ncap2_base_args,
                                     operator_gerund, value, dimension_name, 
                                     file_num, lfl)
                
                print_format_string(prefmt_str_progress_BTH, format_args_print)
                
                # Get the command from the corresponding switch case dictionary #
                format_args = (ncap2_base_args,
                               dimension_name, dimension_name, value,
                               file_name, temp_file)
                
                dimval_mod_formatted = \
                format_string(varval_mod_command_templates_all
                              .get(operator)
                              .get(threshold_mode)
                              .get(use_integer_format),
                              format_args)
            
                # Execute the command through the shell #
                process_exit_info = run_system_command(dimval_mod_formatted,
                                                       capture_output=True,
                                                       encoding="utf-8")
                exit_info(process_exit_info)    
                rename_objects(temp_file, file_name)

            
#--------------------------#
# Parameters and constants #
#--------------------------#

# Template strings #
#------------------#

# NCAP2 command #
ncap2_base_args = "ncap2 -O -s"

# Progress verbose #
prefmt_str_progress_UV = \
"""{} the value of {} to '{}' variable's value for file
{} out of {}..."""

prefmt_str_progress_BTH = \
"""{}, where necessary, the value of {} to '{}' dimension's values for file
{} out of {}..."""

prefmt_str_progress_all = \
"""{} the value of {} to '{}' dimension's values for file
{} out of {}..."""

# NCAP2 command's argument syntaxes, for all values or dimensions #
addvalue_command_template = """{} '{}={}+{}' '{}' '{}'"""
subtrvalue_command_template = """{} '{}={}-{}' '{}' '{}'"""
multvalue_command_template = """{} '{}={}*{}' '{}' '{}'"""
divvalue_command_template = """{} '{}={}/{}' '{}' '{}'"""

addvalue_float_command_template = """{} '{}={}+{}.0f' '{}' '{}'"""
subtrvalue_float_command_template = """{} '{}={}-{}.0f' '{}' '{}'"""
multvalue_float_command_template = """{} '{}={}*{}.0f' '{}' '{}'"""
divvalue_float_command_template = """{} '{}={}/{}.0f' '{}' '{}'"""

# NCAP2 command's argument syntaxes, conditional #
addvalue_where_max_command_template = """{} 'where({}<{}) {}={}+{}' '{}' '{}'"""
subtrvalue_where_max_command_template = """{} 'where({}<{}) {}={}-{}' '{}' '{}'"""
multvalue_where_max_command_template = """{} 'where({}<{}) {}={}*{}' '{}' '{}'"""
divvalue_where_max_command_template = """{} 'where({}<{}) {}={}/{}' '{}' '{}'"""

addvalue_where_max_float_command_template = """{} 'where({}<{}) {}={}+{}.0f' '{}' '{}'"""
subtrvalue_where_max_float_command_template = """{} 'where({}<{}) {}={}-{}.0f' '{}' '{}'"""
multvalue_where_max_float_command_template = """{} 'where({}<{}) {}={}*{}.0f' '{}' '{}'"""
divvalue_where_max_float_command_template = """{} 'where({}<{}) {}={}/{}.0f' '{}' '{}'"""


addvalue_where_min_command_template = """{} 'where({}>{}) {}={}+{}' '{}' '{}'"""
subtrvalue_where_min_command_template = """{} 'where({}>{}) {}={}-{}' '{}' '{}'"""
multvalue_where_min_command_template = """{} 'where({}>{}) {}={}*{}' '{}' '{}'"""
divvalue_where_min_command_template = """{} 'where({}>{}) {}={}/{}' '{}' '{}'"""

addvalue_where_min_float_command_template = """{} 'where({}>{}) {}={}+{}.0f' '{}' '{}'"""
subtrvalue_where_min_float_command_template = """{} 'where({}>{}) {}={}-{}.0f' '{}' '{}'"""
multvalue_where_min_float_command_template = """{} 'where({}>{}) {}={}*{}.0f' '{}' '{}'"""
divvalue_where_min_float_command_template = """{} 'where({}>{}) {}={}/{}.0f' '{}' '{}'"""

# Fixed strings #
#---------------#

# Error messages #
invalid_operator_err_template = \
f"Invalid basic operator chosen. Options are {basic_four_rules}."
invalid_threshold_mode_err_template = \
"""Invalid threshold mode. Options are {}."""


# Locally available threshold mode list #
#---------------------------------------#

threshold_mode_opts = ["max", "min"]

# Switch case dictionaries #
#--------------------------#

operator_gerund_dict = {
    basic_four_rules[0] : "Adding",
    basic_four_rules[1] : "Subtracting",
    basic_four_rules[2] : "Multiplying",
    basic_four_rules[3] : "Dividing"
    }

varval_mod_command_templates_UV = {
    basic_four_rules[0] : {
        1 : addvalue_command_template,
        0 : addvalue_float_command_template
    },
    basic_four_rules[1] : {
        1 : subtrvalue_command_template,
        0 : subtrvalue_float_command_template
    },
    basic_four_rules[2] : {
        1 : multvalue_command_template,
        0 : multvalue_float_command_template
    },
    basic_four_rules[3] : {
        1 : divvalue_command_template,
        0 : divvalue_float_command_template
    }
}

varval_mod_command_templates_BTH = {
    basic_four_rules[0] : {
        "max" : {
            1 : addvalue_where_max_command_template,
            0 : addvalue_where_max_float_command_template
        },
        "min" : {
            1 : addvalue_where_min_command_template,
            0 : addvalue_where_min_float_command_template
        },
    },
    basic_four_rules[1] : {
        "max" : {
            1 : subtrvalue_where_max_command_template,
            0 : subtrvalue_where_max_float_command_template
        },
        "min" : {
            1 : subtrvalue_where_min_command_template,
            0 : subtrvalue_where_min_float_command_template
        },
    },
    basic_four_rules[2] : {
        "max" : {
            1 : multvalue_where_max_command_template,
            0 : multvalue_where_max_float_command_template
        },
        "min" : {
            1 : multvalue_where_min_command_template,
            0 : multvalue_where_min_float_command_template
        },
    },
    basic_four_rules[3] : {
        "max" : {
            1 : divvalue_where_max_command_template,
            0 : divvalue_where_max_float_command_template
        },
        "min" : {
            1 : divvalue_where_min_command_template,
            0 : divvalue_where_min_float_command_template
        }
    }
}

varval_mod_command_templates_all = {
    basic_four_rules[0] : {
        "max" : {
            1 : addvalue_command_template,
            0 : addvalue_float_command_template
        },
        "min" : {
            1 : addvalue_command_template,
            0 : addvalue_float_command_template
        },
    },
    basic_four_rules[1] : {
        "max" : {
            1 : subtrvalue_command_template,
            0 : subtrvalue_float_command_template
        },
        "min" : {
            1 : subtrvalue_command_template,
            0 : subtrvalue_float_command_template
        },
    },
    basic_four_rules[2] : {
        "max" : {
            1 : multvalue_command_template,
            0 : multvalue_float_command_template
        },
        "min" : {
            1 : multvalue_command_template,
            0 : multvalue_float_command_template
        },
    },
    basic_four_rules[3] : {
        "max" : {
            1 : divvalue_command_template,
            0 : divvalue_float_command_template
        },
        "min" : {
            1 : divvalue_command_template,
            0 : divvalue_float_command_template
        }
    }
}
