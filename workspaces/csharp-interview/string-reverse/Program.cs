// ============================================================
// C# Interview Question - Top 5 Coding Questions #1
// "Write a program in C# to reverse a string"
// Source: SimplyLearn - C# Interview Questions and Answers
// ============================================================

using System;

namespace CSharpInterview
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Enter a string to reverse:");
            string input = Console.ReadLine();
            Console.WriteLine("Reversed string: " + ReverseString(input));
        }

        static string ReverseString(string input)
        {
            char[] charArray = input.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }
    }
}