#pragma once

#include <string>
#include <array>
#include <type_traits>

template<typename T>
using array_elem_type = std::remove_reference_t<decltype(std::declval<T>()[0])>;

template<typename T>
constexpr auto array_elem_count = sizeof(std::declval<T>()) / sizeof(std::declval<T>()[0]);

#define FIELD(OFFSET, TYPE, NAME) \
    void set_##NAME(std::add_const_t<std::add_lvalue_reference_t<TYPE>> value) \
    { \
        *(std::add_pointer_t<TYPE>)((char*)this + OFFSET) = value; \
    } \
    \
    void set_##NAME(std::add_rvalue_reference_t<TYPE> value) \
    { \
        *(std::add_pointer_t<TYPE>)((char*)this + OFFSET) = std::move(value); \
    } \
    \
    std::add_lvalue_reference_t<TYPE> get_##NAME() const \
    { \
        return *(std::add_pointer_t<TYPE>)((char*)this + OFFSET); \
    } \
    __declspec(property(get=get_##NAME, put=set_##NAME)) TYPE NAME

#define ARRAY_FIELD(OFFSET, TYPE, NAME) \
    void set_##NAME(int index, std::add_const_t<std::add_lvalue_reference_t<array_elem_type<TYPE>>> value) \
    { \
        (reinterpret_cast<array_elem_type<TYPE>*>((char*)this + OFFSET))[index] = value; \
    } \
    \
    void set_##NAME(int index, std::add_rvalue_reference_t<array_elem_type<TYPE>> value) \
    { \
        (reinterpret_cast<array_elem_type<TYPE>*>((char*)this + OFFSET))[index] = std::move(value); \
    } \
    \
    std::add_lvalue_reference_t<array_elem_type<TYPE>> get_##NAME(int index) const \
    { \
        return (reinterpret_cast<array_elem_type<TYPE>*>((char*)this + OFFSET))[index]; \
    } \
    __declspec(property(get=get_##NAME, put=set_##NAME)) array_elem_type<TYPE> NAME[array_elem_count<TYPE>]

#define BIT_FIELD(OFFSET, MASK, NAME) \
    void set_##NAME(bool value) \
    { \
        if (value) \
            *(int*)((char*)this + OFFSET) |= MASK; \
        else \
            *(int*)((char*)this + OFFSET) &= ~MASK; \
    } \
    \
    bool get_##NAME() const \
    { \
        return (*(int*)((char*)this + OFFSET) & MASK) != 0; \
    } \
    __declspec(property(get=get_##NAME, put=set_##NAME)) bool NAME